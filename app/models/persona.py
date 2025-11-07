"""
Persona data models using Pydantic for validation and serialization.
"""

from pydantic import BaseModel, Field, HttpUrl, validator
from typing import Optional, Any, Dict, List
from uuid import UUID
from datetime import datetime


class PersonaBase(BaseModel):
    """Base persona model with common fields."""

    raw_text: str = Field(..., description="Original unstructured text input")
    persona: Optional[Dict[str, Any]] = Field(None, description="Structured persona JSON output")


class PersonaCreate(BaseModel):
    """
    Model for creating a new persona.

    Supports flexible input sources:
    - raw_text: Direct text input for persona generation
    - urls: 1-10 URLs containing persona information

    At least one source (raw_text or urls) must be provided.
    """

    raw_text: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50000,
        description="Raw text containing persona information"
    )
    urls: Optional[List[HttpUrl]] = Field(
        None,
        min_items=1,
        max_items=10,
        description="URLs containing persona information (1-10 URLs)"
    )

    @validator('urls', pre=True, always=True)
    def at_least_one_input(cls, v, values):
        """Ensure at least one input source is provided."""
        raw_text = values.get('raw_text')
        if not raw_text and (v is None or len(v) == 0):
            raise ValueError(
                'Either raw_text or urls must be provided. '
                'Provide raw text directly or 1-10 URLs containing persona information.'
            )
        return v

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "raw_text": "John is a software engineer with 10 years of experience in full-stack development..."
                },
                {
                    "urls": ["https://example.com/bio", "https://example.com/resume"]
                },
                {
                    "raw_text": "Additional context about the person...",
                    "urls": ["https://example.com/profile"]
                }
            ]
        }


class PersonaUpdate(BaseModel):
    """Model for updating an existing persona."""

    raw_text: Optional[str] = Field(None, description="Updated raw text")
    persona: Optional[Dict[str, Any]] = Field(None, description="Updated persona JSON")


class PersonaInDB(PersonaBase):
    """Model for persona as stored in database."""

    id: UUID = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True


class PersonaResponse(PersonaInDB):
    """Model for API responses."""

    pass


class PersonaCreateResponse(BaseModel):
    """
    Response model for POST /v1/persona endpoint (201 Created).

    Only includes essential metadata about the created persona.
    raw_text and persona JSON are excluded to minimize payload size
    and optimize API response time.

    Fields:
        id: Unique identifier of the created persona
        created_at: ISO 8601 timestamp when the persona was created
        updated_at: ISO 8601 timestamp when the persona was last updated
    """

    id: str = Field(..., description="Unique identifier of the created persona")
    created_at: datetime = Field(..., description="Creation timestamp (ISO 8601)")
    updated_at: datetime = Field(..., description="Last update timestamp (ISO 8601)")

    class Config:
        from_attributes = True


class PersonaListResponse(BaseModel):
    """Model for listing personas."""

    items: list[PersonaInDB] = Field(..., description="List of personas")
    total: int = Field(..., description="Total count of personas")
    limit: int = Field(..., description="Items per page")
    offset: int = Field(..., description="Pagination offset")
