"""
Person data models using Pydantic for validation and serialization.

Represents the person aggregate root in the domain model.
"""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class PersonBase(BaseModel):
    """
    Base person model with common fields.

    Minimal aggregate root with just identity information.
    Related data (submissions, computed personas) are accessed via person_id.
    """

    first_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="First name of the person"
    )
    last_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Last name of the person"
    )
    gender: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        description="Gender of the person (e.g., male, female, other, prefer not to say)"
    )


class PersonCreate(PersonBase):
    """
    Model for creating a new person.

    Creates the aggregate root with optional demographic information.
    Data submissions are added subsequently via separate endpoints.
    """

    pass  # Inherits first_name, last_name, gender from PersonBase


class PersonInDB(PersonBase):
    """
    Model for person as stored in database.

    Represents the aggregate root with its identity and timestamps.
    Related data and personas are accessed via foreign keys.
    """

    id: UUID = Field(..., description="Unique identifier (UUID v4)")
    created_at: datetime = Field(..., description="Timestamp when person record created")
    updated_at: datetime = Field(..., description="Timestamp when person record last updated")

    class Config:
        from_attributes = True


class PersonResponse(PersonInDB):
    """
    Model for person API responses.

    Includes computed metadata about the person's data and personas.
    """

    person_data_count: int = Field(
        default=0,
        description="Number of unstructured data submissions for this person"
    )
    latest_persona_version: Optional[int] = Field(
        default=None,
        description="Version number of the latest computed persona (None if no persona yet)"
    )

    class Config:
        from_attributes = True
