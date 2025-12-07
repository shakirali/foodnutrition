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

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import AppConfig
from agents.advisor_agent import NutritionAdvisorAgent
from spoon_ai.chat import ChatBot


# Global agent instance
agent: Optional[NutritionAdvisorAgent] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    global agent
    try:
        AppConfig.validate()
        agent = NutritionAdvisorAgent(
            llm=ChatBot(
                llm_provider=AppConfig.DEFAULT_LLM_PROVIDER,
                model=AppConfig.DEFAULT_LLM_MODEL
            )
        )
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
    allow_origins=["*"],  # In production, specify actual origins
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
    """Update user profile (placeholder for future implementation)."""
    # Profile storage will be implemented in a future update
    return {"status": "success", "message": "Profile updated"}


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "agent_initialized": agent is not None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

