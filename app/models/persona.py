"""
Persona data models using Pydantic for validation and serialization.
"""

from pydantic import BaseModel, Field, HttpUrl, validator
from typing import Optional, Any, Dict, List, Union
from uuid import UUID
from datetime import datetime


class PersonaBase(BaseModel):
    """
    Base persona model with common fields.

    Represents a computed persona with version tracking and data lineage.
    """

    persona: Dict[str, Any] = Field(..., description="Structured persona JSON output")


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
    """
    Model for persona as stored in database.

    Includes person_id for aggregate root reference, version for tracking
    persona recomputations, and computed_from_data_ids for data lineage.
    """

    id: UUID = Field(..., description="Unique identifier")
    person_id: UUID = Field(..., description="Foreign key to persons table (aggregate root)")
    version: int = Field(
        default=1,
        description="Version number (increments with each recomputation). Starts at 1."
    )
    computed_from_data_ids: List[UUID] = Field(
        default_factory=list,
        description="UUID array of person_data IDs used in this computation (lineage tracking)"
    )
    created_at: datetime = Field(..., description="When persona first computed for this person")
    updated_at: datetime = Field(..., description="When persona last recomputed")

    class Config:
        from_attributes = True


class PersonaResponse(PersonaInDB):
    """Model for API responses."""

    pass


class PersonaWithHistory(PersonaResponse):
    """
    Model for persona response with source data history.

    Includes the complete person_data records that were used to
    compute this persona, enabling full audit trail and lineage.
    """

    computed_from_data: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Person_data submission records used to compute this persona"
    )


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


class ErrorResponse(BaseModel):
    """
    Standard error response model.

    Returned when an error occurs during API request processing.
    Includes detailed error information for debugging and client handling.
    """

    error: str = Field(..., description="Error message with detailed information")
    error_type: str = Field(..., description="Type of error (e.g., 'ValueError', 'ValidationError')")
    status_code: int = Field(..., description="HTTP status code")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when error occurred (ISO 8601)")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Persona not found with ID: 550e8400-e29b-41d4-a716-446655440000",
                "error_type": "ValueError",
                "status_code": 404,
                "timestamp": "2024-11-08T10:30:45.123456"
            }
        }
