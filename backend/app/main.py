"""
Master FastAPI Application for SIH 2026 Problem Statement 26086.
Hyperlocal Monsoon Onset & Break Prediction System (Ministry of Earth Sciences / NCMRWF).
"""

import os
import secrets
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from backend.app.core.config import settings
from backend.app.db.database import init_db, seed_blocks_if_empty
from backend.app.api.endpoints import router as api_router
from backend.app.api.prediction_router import router as prediction_router
from backend.app.api.agent_router import router as agent_router

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
BLOCKS_GEOJSON = os.path.join(BASE_DIR, "data", "admin_boundaries", "blocks_sample.geojson")

# Rate Limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
<div style="background:#15803d; color:#ffffff; padding:18px 22px; border-radius:10px; margin-bottom:20px; font-family:sans-serif;">
  <h3 style="color:#ffffff; margin:0 0 8px 0; font-size:20px;">🌾 Looking for the Interactive Frontend Web App?</h3>
  <p style="margin:0 0 14px 0; color:#dcfce7; font-size:14px;">
    You are currently viewing the raw OpenAPI / Swagger backend developer documentation.
    To use the full interactive map, state/district weather predictions, and Kisan AI assistant, open:
  </p>
  <a href="/" target="_self" style="display:inline-block; background:#ffffff; color:#15803d; font-weight:800; padding:10px 20px; border-radius:8px; text-decoration:none; font-size:15px; box-shadow:0 3px 8px rgba(0,0,0,0.2);">
    👉 OPEN FULL FRONTEND WEB APPLICATION (http://localhost:8000/)
  </a>
</div>

*Ministry of Earth Sciences (MoES / NCMRWF) Hyperlocal Monsoon Prediction & Agromet Advisory Engine.*
""",
    docs_url="/docs-api",
    redoc_url="/redoc"
)

@app.get("/docs", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(url="/docs-api")


from starlette.middleware.gzip import GZipMiddleware

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Gzip compression for all text/html/json/js/css responses over 1KB
app.add_middleware(GZipMiddleware, minimum_size=1000)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def manage_cache_headers(request, call_next):
    response = await call_next(request)
    path = request.url.path.lower()
    # Cache versioned JS, CSS, images and fonts for high performance
    if any(path.endswith(ext) for ext in [".js", ".css", ".png", ".jpg", ".jpeg", ".svg", ".webp", ".woff", ".woff2", ".ico"]):
        response.headers["Cache-Control"] = "public, max-age=86400"
    # Ensure index.html and root URL always revalidate to receive latest updates
    elif path == "/" or path.endswith(".html"):
        response.headers["Cache-Control"] = "no-cache, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response

# Basic Auth Security for Officials Dashboard
security = HTTPBasic()


def verify_officials_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, settings.OFFICIALS_USER)
    correct_password = secrets.compare_digest(credentials.password, settings.OFFICIALS_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password for Officials Dashboard access",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


# Include API Routers
app.include_router(api_router, prefix="/api")
app.include_router(agent_router, prefix="/api")
app.include_router(prediction_router)  # Direct /predict/block/{block_id}
app.include_router(prediction_router, prefix="/api")  # /api/predict/block/{block_id}


@app.on_event("startup")
def startup_event():
    init_db()
    seed_blocks_if_empty(BLOCKS_GEOJSON)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "hosting_tier": settings.HOSTING_TIER,
        "cold_start_mitigation": settings.COLD_START_NOTE,
        "privacy_notice": settings.PRIVACY_CONSENT_NOTICE
    }


# Mount Frontend if directory exists
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
