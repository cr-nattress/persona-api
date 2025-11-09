"""
Person data models for unstructured data submissions.

Represents the history of unstructured data submissions for a person.
Each record = one API call with all data sent in that call.
"""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class PersonDataBase(BaseModel):
    """
    Base person data model with common fields.

    Represents a single unstructured data submission.
    """

    raw_text: str = Field(
        ...,
        min_length=1,
        max_length=100000,
        description="Complete unstructured text submitted in this API call"
    )
    source: str = Field(
        default="api",
        description="Source of data (api, urls, import, etc). Defaults to api."
    )


class PersonDataCreate(PersonDataBase):
    """
    Model for creating a new person data submission.

    When adding data to a person, include the raw_text and optional source.
    The person_id is provided via the URL path parameter.
    """

    person_id: Optional[UUID] = Field(
        None,
        description="Person ID this data belongs to (provided in URL path)"
    )


class PersonDataInDB(PersonDataBase):
    """
    Model for person data as stored in database.

    Represents a historical submission of unstructured data.
    Includes all metadata: id, person_id, created_at timestamp.
    """

    id: UUID = Field(..., description="Unique identifier for this submission")
    person_id: UUID = Field(..., description="Foreign key to persons table")
    created_at: datetime = Field(..., description="Timestamp when data was submitted")

    class Config:
        from_attributes = True


class PersonDataResponse(PersonDataInDB):
    """
    Model for person data API responses.

    Full submission record with history and lineage information.
    """

    pass


class PersonDataListResponse(BaseModel):
    """Model for listing person data with pagination."""

    items: list[PersonDataInDB] = Field(..., description="List of data submissions")
    total: int = Field(..., description="Total count of submissions for this person")
    limit: int = Field(..., description="Items per page")
    offset: int = Field(..., description="Pagination offset")
