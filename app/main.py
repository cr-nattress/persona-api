"""
FastAPI application initialization.

Main entry point for the Persona-API server.
"""

from fastapi import FastAPI, Request, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from contextlib import asynccontextmanager
from datetime import datetime
from app.core import settings, setup_logging, get_logger
from app.core.logging import set_correlation_id, get_correlation_id
from app.core.exceptions import validation_exception_handler, http_exception_handler, general_exception_handler
from app.api import router as persona_router
from app.api.person_routes import router as person_router

# Initialize logging
setup_logging(log_level=settings.log_level, environment=settings.environment)
logger = get_logger(__name__)


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """Middleware to handle correlation IDs for request tracing."""

    async def dispatch(self, request: Request, call_next):
        # Check for correlation ID in request headers
        corr_id = request.headers.get("x-correlation-id")
        if not corr_id:
            corr_id = get_correlation_id()
        else:
            set_correlation_id(corr_id)

        # Process request
        response = await call_next(request)

        # Add correlation ID to response headers
        response.headers["X-Correlation-ID"] = corr_id
        return response


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
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add correlation ID middleware (before CORS)
app.add_middleware(CorrelationIDMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(persona_router)
app.include_router(person_router)

# Register exception handlers
# Order matters: more specific handlers should come before general ones
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


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


@app.post("/migrate", tags=["Admin"])
async def run_migration():
    """
    Apply pending database migrations (development only).

    This endpoint applies the 002_create_person_aggregate_schema.sql migration
    to add first_name, last_name, and gender columns to the persons table.
    """
    import os
    from pathlib import Path

    if not settings.is_development:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Migration endpoint only available in development mode"
        )

    try:
        # Read migration file
        migration_path = Path(__file__).parent.parent / "db" / "migrations" / "002_create_person_aggregate_schema.sql"
        if not migration_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Migration file not found: {migration_path}"
            )

        with open(migration_path, 'r') as f:
            sql_content = f.read()

        # For now, return the SQL that needs to be applied
        logger.warning("Migration endpoint called - SQL content prepared for manual execution")

        return {
            "status": "pending",
            "message": "Migration SQL prepared",
            "migration_file": "002_create_person_aggregate_schema.sql",
            "instructions": "This migration needs to be applied manually via Supabase dashboard SQL Editor",
            "sql_content": sql_content
        }

    except Exception as e:
        logger.error(f"Migration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Migration failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=settings.is_development,
        log_level=settings.log_level.lower(),
    )
