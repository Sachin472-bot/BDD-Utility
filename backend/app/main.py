from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .api import api_router

app = FastAPI(title="BDD Utility API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory for uploaded files
static_path = Path(__file__).parent / "static"
static_path.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Include API router
app.include_router(api_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to BDD Utility API",
        "docs_url": "/docs",
        "endpoints": [
            {"path": "/api/convert-to-feature", "method": "POST", "description": "Convert document to feature file"},
            {"path": "/api/generate-steps", "method": "POST", "description": "Generate step definitions"}
        ]
    }