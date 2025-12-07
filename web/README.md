# Web Interface for Nutrition Advisor

This directory contains the web interface for the Nutrition-Based Local Food Advisor App.

## Structure

```
web/
├── __init__.py
├── api.py              # FastAPI backend
├── run_server.py       # Server startup script
├── templates/
│   └── index.html      # Main HTML page
└── static/
    ├── css/
    │   └── style.css   # Stylesheet
    └── js/
        └── app.js      # Frontend JavaScript
```

## Installation

Make sure you have installed all dependencies:

```bash
pip install -r requirements.txt
```

## Running the Web Server

### Option 1: Using the run script

```bash
python web/run_server.py
```

### Option 2: Using uvicorn directly

```bash
uvicorn web.api:app --host 0.0.0.0 --port 8000 --reload
```

### Option 3: Using Python module

```bash
python -m uvicorn web.api:app --host 0.0.0.0 --port 8000 --reload
```

## Accessing the Application

Once the server is running, open your browser and navigate to:

- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## Features

- **Chat Interface**: Conversational AI interface for nutrition advice
- **Quick Actions**: Pre-defined action buttons for common queries
- **Dark Mode**: Toggle between light and dark themes
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Chat**: Instant responses from the AI agent

## API Endpoints

- `GET /`: Main web interface
- `POST /api/chat`: Send chat messages
- `POST /api/profile`: Update user profile (placeholder)
- `GET /api/health`: Health check endpoint

## Development

The web interface uses:
- **Backend**: FastAPI (Python)
- **Frontend**: Vanilla JavaScript (no framework dependencies)
- **Styling**: CSS with CSS variables for theming

### Development Mode

The server runs with `--reload` flag by default, which automatically restarts when code changes are detected.

## Environment Variables

Make sure your `.env` file is configured with:
- `DEFAULT_LLM_PROVIDER`
- `DEFAULT_LLM_API_KEY` (or `OPENAI_API_KEY`)
- `DEFAULT_LLM_MODEL`
- `DEFAULT_LLM_TEMPERATURE`

See the main `README.md` for details.

