"""
Persona service - high-level business logic for persona operations.

Coordinates persona synthesis, validation, merging, and advanced operations.
Builds on PersonaSynthesizer for core functionality.
"""

from typing import Dict, Any, List, Optional, Tuple
from uuid import UUID
from datetime import datetime
from app.models.persona import PersonaInDB, PersonaCreate
from app.services.persona_synthesizer import PersonaSynthesizer, get_persona_synthesizer
from app.repositories.persona_repo import get_persona_repository
from app.core.logging import get_logger

logger = get_logger(__name__)


class PersonaService:
    """High-level business service for persona operations."""

    def __init__(self, synthesizer: Optional[PersonaSynthesizer] = None):
        """
        Initialize PersonaService.

        Args:
            synthesizer: Optional PersonaSynthesizer instance (uses singleton if not provided)
        """
        self.synthesizer = synthesizer or get_persona_synthesizer()
        self.repository = get_persona_repository()

    async def generate_persona(self, raw_text: str) -> PersonaInDB:
        """
        Generate and save a new persona.

        Args:
            raw_text: Unstructured text about a person

        Returns:
            PersonaInDB: Created persona with ID and metadata

        Raises:
            ValueError: If generation fails
        """
        logger.info("PersonaService: Generating new persona")
        return await self.synthesizer.generate_and_save_persona(raw_text)

    async def update_persona(self, persona_id: str, new_raw_text: str) -> PersonaInDB:
        """
        Update persona with new information.

        Args:
            persona_id: UUID of persona to update
            new_raw_text: New or updated text about the person

        Returns:
            PersonaInDB: Updated persona

        Raises:
            ValueError: If update fails or persona not found
        """
        logger.info(f"PersonaService: Updating persona {persona_id}")
        return await self.synthesizer.regenerate_persona(persona_id, new_raw_text)

    async def get_persona(self, persona_id: str) -> PersonaInDB:
        """
        Retrieve a persona by ID.

        Args:
            persona_id: UUID of persona

        Returns:
            PersonaInDB: The persona

        Raises:
            ValueError: If persona not found
        """
        logger.debug(f"PersonaService: Getting persona {persona_id}")
        return await self.synthesizer.get_persona(persona_id)

    async def list_personas(
        self, limit: int = 10, offset: int = 0
    ) -> Tuple[List[PersonaInDB], int]:
        """
        List personas with pagination.

        Args:
            limit: Items per page (1-100)
            offset: Items to skip

        Returns:
            Tuple of (personas list, total count)

        Raises:
            ValueError: If listing fails
        """
        logger.debug(f"PersonaService: Listing personas (limit={limit}, offset={offset})")
        return await self.synthesizer.list_personas(limit, offset)

    async def delete_persona(self, persona_id: str) -> bool:
        """
        Delete a persona.

        Args:
            persona_id: UUID of persona to delete

        Returns:
            True if deleted, False if not found

        Raises:
            ValueError: If deletion fails
        """
        logger.info(f"PersonaService: Deleting persona {persona_id}")
        return await self.synthesizer.delete_persona(persona_id)

    async def merge_personas(
        self, persona_id_1: str, persona_id_2: str, merged_raw_text: Optional[str] = None
    ) -> PersonaInDB:
        """
        Merge two personas into one.

        Combines information from both personas and optionally regenerates
        with merged raw text. The first persona's ID is used for the merged result.

        Args:
            persona_id_1: UUID of first persona (becomes the merged result)
            persona_id_2: UUID of second persona (will be deleted)
            merged_raw_text: Optional new raw text combining both personas.
                           If not provided, uses concatenation of both.

        Returns:
            PersonaInDB: Merged persona with combined information

        Raises:
            ValueError: If merge fails or personas not found
        """
        try:
            logger.info(f"PersonaService: Merging personas {persona_id_1} and {persona_id_2}")

            # Retrieve both personas
            persona_1 = await self.get_persona(persona_id_1)
            persona_2 = await self.get_persona(persona_id_2)

            # If no merged text provided, combine both raw texts
            if merged_raw_text is None:
                merged_raw_text = f"{persona_1.raw_text}\n\n---\n\n{persona_2.raw_text}"
                logger.debug("Generated merged raw text from both personas")
            else:
                logger.debug("Using provided merged raw text")

            # Regenerate with merged information
            merged_persona = await self.synthesizer.regenerate_persona(
                persona_id_1, merged_raw_text
            )

            # Delete the second persona
            await self.synthesizer.delete_persona(persona_id_2)
            logger.info(f"PersonaService: Merge complete. Deleted {persona_id_2}")

            return merged_persona

        except Exception as e:
            logger.error(f"PersonaService: Merge failed: {e}")
            raise ValueError(f"Failed to merge personas: {e}") from e

    async def batch_generate_personas(
        self, raw_texts: List[str]
    ) -> List[PersonaInDB]:
        """
        Generate multiple personas in sequence.

        Args:
            raw_texts: List of unstructured text entries

        Returns:
            List of created personas

        Raises:
            ValueError: If any generation fails
        """
        try:
            logger.info(f"PersonaService: Batch generating {len(raw_texts)} personas")
            personas = []

            for i, raw_text in enumerate(raw_texts, 1):
                logger.debug(f"Batch progress: {i}/{len(raw_texts)}")
                persona = await self.synthesizer.generate_and_save_persona(raw_text)
                personas.append(persona)

            logger.info(f"PersonaService: Batch complete. Generated {len(personas)} personas")
            return personas

        except Exception as e:
            logger.error(f"PersonaService: Batch generation failed: {e}")
            raise ValueError(f"Failed to batch generate personas: {e}") from e

    async def search_personas(self, query: str, limit: int = 10) -> List[PersonaInDB]:
        """
        Search for personas by name, role, or other fields.

        Simple text search across persona metadata and fields.

        Args:
            query: Search query (name, role, keywords)
            limit: Maximum results to return

        Returns:
            List of matching personas

        Raises:
            ValueError: If search fails
        """
        try:
            logger.debug(f"PersonaService: Searching personas for '{query}'")

            # Get all personas (in production, would use database search)
            all_personas, _ = await self.synthesizer.list_personas(limit=1000, offset=0)

            # Filter by query
            query_lower = query.lower()
            results = []

            for persona in all_personas:
                # Search in raw text
                if query_lower in persona.raw_text.lower():
                    results.append(persona)
                    continue

                # Search in persona meta data (name, role, location)
                if isinstance(persona.persona, dict):
                    meta = persona.persona.get("meta", {})
                    identity = persona.persona.get("identity", {})

                    if query_lower in str(meta.get("name", "")).lower():
                        results.append(persona)
                    elif query_lower in str(meta.get("role", "")).lower():
                        results.append(persona)
                    elif query_lower in str(meta.get("location", "")).lower():
                        results.append(persona)
                    elif query_lower in str(identity.get("core_description", "")).lower():
                        results.append(persona)

            logger.info(f"PersonaService: Found {len(results)} matching personas")
            return results[:limit]

        except Exception as e:
            logger.error(f"PersonaService: Search failed: {e}")
            raise ValueError(f"Failed to search personas: {e}") from e

    async def get_persona_stats(self) -> Dict[str, Any]:
        """
        Get statistics about personas in the system.

        Returns:
            Dictionary with stats (total count, creation dates, etc.)

        Raises:
            ValueError: If stats retrieval fails
        """
        try:
            logger.debug("PersonaService: Calculating persona statistics")

            _, total = await self.synthesizer.list_personas(limit=1, offset=0)

            # If no personas, return empty stats
            if total == 0:
                stats = {
                    "total_personas": 0,
                    "oldest_created": None,
                    "newest_created": None,
                    "days_active": 0,
                }
                logger.info("PersonaService: No personas in system")
                return stats

            # Get all personas for date analysis
            all_personas, _ = await self.synthesizer.list_personas(limit=10000, offset=0)

            if not all_personas:
                stats = {
                    "total_personas": total,
                    "oldest_created": None,
                    "newest_created": None,
                    "days_active": 0,
                }
            else:
                # Calculate stats
                dates = [p.created_at for p in all_personas]
                oldest = min(dates)
                newest = max(dates)

                stats = {
                    "total_personas": total,
                    "oldest_created": oldest.isoformat(),
                    "newest_created": newest.isoformat(),
                    "days_active": (newest - oldest).days,
                }

            logger.info(f"PersonaService: Stats - {stats}")
            return stats

        except Exception as e:
            logger.error(f"PersonaService: Stats retrieval failed: {e}")
            raise ValueError(f"Failed to get persona stats: {e}") from e

    async def export_personas(
        self, format: str = "json", limit: int = 1000
    ) -> Dict[str, Any]:
        """
        Export personas in specified format.

        Args:
            format: Export format ('json', 'csv' planned)
            limit: Maximum personas to export

        Returns:
            Exported data in requested format

        Raises:
            ValueError: If export fails or format invalid
        """
        try:
            if format != "json":
                raise ValueError(f"Unsupported export format: {format}")

            logger.info(f"PersonaService: Exporting personas as {format}")

            personas, total = await self.synthesizer.list_personas(limit=limit, offset=0)

            export_data = {
                "export_format": format,
                "exported_at": datetime.now().isoformat(),
                "total_exported": len(personas),
                "total_in_system": total,
                "personas": [p.model_dump() for p in personas],
            }

            logger.info(f"PersonaService: Exported {len(personas)} personas")
            return export_data

        except Exception as e:
            logger.error(f"PersonaService: Export failed: {e}")
            raise ValueError(f"Failed to export personas: {e}") from e


def get_persona_service(synthesizer: Optional[PersonaSynthesizer] = None) -> PersonaService:
    """
    Get a PersonaService instance.

    Args:
        synthesizer: Optional PersonaSynthesizer to use (uses singleton if not provided)

    Returns:
        PersonaService instance

    Usage:
        from app.services.persona_service import get_persona_service
        service = get_persona_service()
        persona = await service.generate_persona(raw_text)
    """
    return PersonaService(synthesizer=synthesizer)
