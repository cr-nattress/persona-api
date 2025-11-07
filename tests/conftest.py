"""
Pytest configuration and shared fixtures for test suite.

Provides fixtures for database, LLM, and API testing.
"""

import pytest
import asyncio
from typing import Generator
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from datetime import datetime

from app.models.persona import PersonaInDB, PersonaCreate
from app.services.persona_service import PersonaService
from app.repositories.persona_repo import PersonaRepository
from app.services.persona_synthesizer import PersonaSynthesizer
from app.services.llm_chain import PersonaLLMChain


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_raw_text() -> str:
    """Sample raw text for testing."""
    return """
    John is a software engineer with 10 years of experience.
    He loves building scalable systems and mentoring junior developers.
    He's passionate about open source and speaks at conferences.
    """


@pytest.fixture
def sample_persona_dict() -> dict:
    """Sample persona JSON structure."""
    return {
        "meta": {
            "name": "John Engineer",
            "role": "Senior Software Engineer",
            "age_range": "30-40",
            "location": "San Francisco, CA",
            "created_at": datetime.now().isoformat(),
        },
        "identity": {
            "core_description": "Passionate software engineer focused on scalability",
            "self_perception": "Technical leader and mentor",
            "archetypes": ["The Architect", "The Mentor"],
            "values": ["Excellence", "Knowledge Sharing", "Innovation"],
            "beliefs": ["Good code is documented code", "People matter more than code"],
        },
        "cognition": {
            "thinking_style": "Analytical and systematic",
            "decision_making": "Data-driven with intuition",
            "learning_style": "Learning by doing",
            "problem_solving": "Breaking problems into components",
            "risk_tolerance": "Calculated risk taker",
        },
        "behavior": {
            "patterns": ["Early riser", "Deep focus", "Collaborative"],
            "habits": ["Code review", "Documentation", "Mentoring"],
            "routines": ["Daily standup", "Weekly planning", "Monthly retrospectives"],
            "social_behavior": "Extroverted but focused",
            "energy_level": "High and consistent",
        },
        "communication": {
            "tone": "Professional yet approachable",
            "style": "Clear and structured",
            "preferences": ["Written documentation", "Code reviews", "1-on-1s"],
            "vocabulary": "Technical with business context",
            "non_verbal": "Active listener, good eye contact",
        },
        "strengths": [
            "System design",
            "Technical mentoring",
            "Problem solving",
            "Communication",
            "Leadership",
        ],
        "challenges": [
            "Perfectionism",
            "Impatience with slow processes",
            "Sometimes over-engineers",
        ],
        "interests": {
            "primary": ["Software architecture", "DevOps", "Open source"],
            "secondary": ["Public speaking", "Writing", "Teaching"],
            "passions": ["Building things that matter", "Growing people"],
        },
        "skills": {
            "hard_skills": ["Python", "Go", "Kubernetes", "AWS", "System Design"],
            "soft_skills": ["Leadership", "Mentoring", "Communication"],
            "expertise": ["Microservices", "Cloud Architecture", "Team Leadership"],
        },
        "motivations": {
            "primary_drives": ["Impact", "Mastery", "Growth"],
            "goals": ["Build world-class teams", "Create innovative solutions"],
            "aspirations": ["CTO", "Open source contributor"],
            "fears": ["Stagnation", "Irrelevance"],
        },
        "relationships": {
            "relational_style": "Supportive and collaborative",
            "role_in_groups": "Technical leader and mentor",
            "preferred_relationships": ["Peer mentoring", "Collaborative partnerships"],
            "influence": "High influence through technical expertise",
        },
    }


@pytest.fixture
def sample_persona_in_db(sample_raw_text, sample_persona_dict) -> PersonaInDB:
    """Create sample PersonaInDB object."""
    persona_id = uuid4()
    now = datetime.now()
    return PersonaInDB(
        id=persona_id,
        raw_text=sample_raw_text,
        persona=sample_persona_dict,
        created_at=now,
        updated_at=now,
    )


@pytest.fixture
def sample_persona_create(sample_raw_text, sample_persona_dict) -> PersonaCreate:
    """Create sample PersonaCreate object."""
    return PersonaCreate(
        raw_text=sample_raw_text,
        persona=sample_persona_dict,
    )


@pytest.fixture
def mock_repository() -> AsyncMock:
    """Create mock PersonaRepository."""
    return AsyncMock(spec=PersonaRepository)


@pytest.fixture
def mock_llm_chain() -> AsyncMock:
    """Create mock PersonaLLMChain."""
    return AsyncMock(spec=PersonaLLMChain)


@pytest.fixture
def mock_synthesizer(mock_repository, mock_llm_chain) -> AsyncMock:
    """Create mock PersonaSynthesizer."""
    synthesizer = AsyncMock(spec=PersonaSynthesizer)
    return synthesizer


@pytest.fixture
def persona_service(mock_synthesizer) -> PersonaService:
    """Create PersonaService with mocked dependencies."""
    service = PersonaService(synthesizer=mock_synthesizer)
    return service


@pytest.fixture
async def test_persona_1(sample_persona_in_db) -> PersonaInDB:
    """First test persona."""
    return sample_persona_in_db


@pytest.fixture
async def test_persona_2(sample_raw_text, sample_persona_dict) -> PersonaInDB:
    """Second test persona (different ID)."""
    persona_id = uuid4()
    now = datetime.now()
    return PersonaInDB(
        id=persona_id,
        raw_text=sample_raw_text + " (variant)",
        persona=sample_persona_dict,
        created_at=now,
        updated_at=now,
    )


# Pytest configuration
def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers",
        "asyncio: mark test as asynchronous"
    )
    config.addinivalue_line(
        "markers",
        "unit: mark test as unit test"
    )
    config.addinivalue_line(
        "markers",
        "integration: mark test as integration test"
    )
