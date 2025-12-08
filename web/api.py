"""FastAPI backend for web interface."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
import sys
from pathlib import Path
from elevenlabs.client import ElevenLabs
import asyncio
from fastapi.responses import StreamingResponse

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import AppConfig
from agents.advisor_agent import NutritionAdvisorAgent
from spoon_ai.chat import ChatBot


# Global agent instance
agent: Optional[NutritionAdvisorAgent] = None
elevenlabs_client: Optional[ElevenLabs] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    global agent
    global elevenlabs_client
    try:
        AppConfig.validate()
        agent = NutritionAdvisorAgent(
            llm=ChatBot(
                llm_provider=AppConfig.DEFAULT_LLM_PROVIDER,
                model=AppConfig.DEFAULT_LLM_MODEL
            )
        )
        try:
            if AppConfig.ELEVENLABS_API_KEY:
                elevenlabs_client = ElevenLabs(api_key=AppConfig.ELEVENLABS_API_KEY)
                print("✓ ElevenLabs client initialized successfully")
            else:
                elevenlabs_client = None
                print("✗ ElevenLabs client not initialized")
        except Exception as e:
            print(f"Error initializing ElevenLabs client: {e}")
            elevenlabs_client = None
        print("✓ Agent initialized successfully for web interface")
    except Exception as e:
        print(f"Error initializing agent: {e}")
        raise
    
    yield


app = FastAPI(
    title="Nutrition Advisor API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str


class UserProfile(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    dietary_restrictions: Optional[List[str]] = None

class TTSRequest(BaseModel):
    text: str
    voice_id: Optional[str] = None
    model_id: Optional[str] = None
    output_format: Optional[str] = None


# Mount static files
static_path = Path(__file__).parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page."""
    html_file = Path(__file__).parent / "templates" / "index.html"
    if html_file.exists():
        return html_file.read_text()
    return """
    <html>
        <head><title>Nutrition Advisor</title></head>
        <body>
            <h1>Nutrition Advisor API</h1>
            <p>API is running. Use /docs for API documentation.</p>
        </body>
    </html>
    """


@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Handle chat messages."""
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    try:
        # Clear agent state for new session if needed
        if message.session_id is None or message.session_id == "new":
            agent.clear()
        
        # Process message
        response_text = await agent.run(message.message)
        
        # Generate session ID (simple implementation)
        session_id = message.session_id or "session_1"
        
        return ChatResponse(
            response=response_text,
            session_id=session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/profile")
async def update_profile(profile: UserProfile):
    """Update user profile."""
    # Profile storage implementation pending
    return {"status": "success", "message": "Profile updated"}


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "agent_initialized": agent is not None
    }


@app.post("/api/tts")
async def text_to_speech(request: TTSRequest):
    """Text to speech endpoint."""
    if elevenlabs_client is None:
        raise HTTPException(status_code=503, detail="ElevenLabs client not initialized")
    
    # Validate input
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if len(request.text) > 5000:
        raise HTTPException(status_code=400, detail="Text too long (max 5000 characters)")
    
    try:
        # Calculate actual values with defaults
        actual_voice_id = request.voice_id or "JBFqnCBsd6RMkjVDRZzb"
        actual_model_id = request.model_id or "eleven_turbo_v2"
        actual_output_format = request.output_format or "mp3_44100_128"
        
        # Convert text to speech
        audio = await asyncio.to_thread(
            elevenlabs_client.text_to_speech.convert,
            text=request.text.strip(),
            voice_id=actual_voice_id,
            model_id=actual_model_id,
            output_format=actual_output_format
        )

        # Determine media type based on actual output format
        media_type_map = {
            "mp3_44100_128": "audio/mpeg",
            "mp3_22050_32": "audio/mpeg",
            "mp3_44100_192": "audio/mpeg",
            "pcm_16000": "audio/pcm",
            "pcm_22050": "audio/pcm",
            "pcm_24000": "audio/pcm",
            "pcm_44100": "audio/pcm"
        }
        media_type = media_type_map.get(actual_output_format, "audio/mpeg")

        # Generator for streaming
        def generate():
            for chunk in audio:
                yield chunk
        
        # Response headers
        headers = {
            "Content-Disposition": "inline; filename=tts.mp3",
            "Cache-Control": "no-cache",
            "Accept-Ranges": "bytes",
        }
        
        return StreamingResponse(
            generate(), 
            media_type=media_type, 
            headers=headers,
        )
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS conversion failed: {str(e)}")
