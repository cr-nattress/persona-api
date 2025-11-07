"""
FastAPI application initialization.

Main entry point for the Persona-API server.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core import settings, setup_logging, get_logger

# Initialize logging
setup_logging(log_level=settings.log_level, environment=settings.environment)
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle.

    Startup: Log initialization
    Shutdown: Cleanup
    """
    # Startup
    logger.info(f"🚀 Persona-API starting in {settings.environment} mode")
    logger.info(f"📝 Logging level: {settings.log_level}")
    logger.debug(f"🤖 Using model: {settings.openai_model}")
    logger.debug(f"🗄️  Supabase URL: {settings.supabase_url[:30]}...")

    yield

    # Shutdown
    logger.info("🛑 Persona-API shutting down")


# Initialize FastAPI app
app = FastAPI(
    title="Persona-API",
    description="Transform raw text into structured persona definitions",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API is running."""
    return {
        "message": "Persona-API is running",
        "version": "1.0.0",
        "environment": settings.environment,
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "persona-api",
        "environment": settings.environment,
    }


@app.get("/docs", tags=["Documentation"])
async def docs_redirect():
    """Swagger UI documentation."""
    return {"message": "API documentation available at /docs"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=settings.is_development,
        log_level=settings.log_level.lower(),
    )
