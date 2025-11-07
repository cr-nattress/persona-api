"""
Persona data models using Pydantic for validation and serialization.
"""

from pydantic import BaseModel, Field
from typing import Optional, Any, Dict
from uuid import UUID
from datetime import datetime


class PersonaBase(BaseModel):
    """Base persona model with common fields."""

    raw_text: str = Field(..., description="Original unstructured text input")
    persona: Optional[Dict[str, Any]] = Field(None, description="Structured persona JSON output")


class PersonaCreate(PersonaBase):
    """Model for creating a new persona."""

    pass


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


class PersonaListResponse(BaseModel):
    """Model for listing personas."""

    items: list[PersonaInDB] = Field(..., description="List of personas")
    total: int = Field(..., description="Total count of personas")
    limit: int = Field(..., description="Items per page")
    offset: int = Field(..., description="Pagination offset")
