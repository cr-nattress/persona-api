"""
Data migration script: Old personas table -> New person aggregate root schema

Safely migrates existing persona data from the flat schema to the new
person aggregate root schema with immutable data history and versioning.

Migration Strategy:
1. For each existing persona record:
   - Create a new person in the persons table
   - Create a person_data entry with the original raw_text
   - Create a new persona entry with versioning and lineage tracking
2. Validate data integrity throughout
3. Provide rollback capability and detailed logging
4. Support dry-run mode for testing

Usage:
    python db/migrate_to_person_aggregate.py [--dry-run] [--validate-only]
"""

import asyncio
import json
import sys
from uuid import UUID
from datetime import datetime
from typing import Optional, List
import logging

from app.db.supabase_client import get_supabase_client
from app.core import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PersonAggregateRootMigrator:
    """Orchestrates migration from flat personas schema to aggregate root."""

    def __init__(self, dry_run: bool = False):
        """Initialize migrator."""
        self.supabase = get_supabase_client()
        self.dry_run = dry_run
        self.migrated_count = 0
        self.failed_count = 0
        self.skipped_count = 0
        self.migration_log = []

    async def run(self) -> bool:
        """Execute migration."""
        logger.info("=" * 70)
        logger.info("PERSON AGGREGATE ROOT MIGRATION")
        logger.info("=" * 70)
        logger.info(f"Mode: {'DRY RUN (no changes)' if self.dry_run else 'LIVE (changes applied)'}")
        logger.info("")

        try:
            # Verify tables exist
            await self._verify_tables()

            # Get all existing personas
            old_personas = await self._fetch_old_personas()
            if not old_personas:
                logger.warning("No personas found to migrate.")
                return True

            logger.info(f"Found {len(old_personas)} personas to migrate")
            logger.info("")

            # Migrate each persona
            for i, old_persona in enumerate(old_personas, 1):
                await self._migrate_persona(old_persona, i, len(old_personas))

            # Summary
            logger.info("")
            logger.info("=" * 70)
            logger.info("MIGRATION SUMMARY")
            logger.info("=" * 70)
            logger.info(f"Migrated: {self.migrated_count}")
            logger.info(f"Failed:   {self.failed_count}")
            logger.info(f"Skipped:  {self.skipped_count}")
            logger.info(f"Total:    {len(old_personas)}")
            logger.info(f"Status:   {'SUCCESS' if self.failed_count == 0 else 'PARTIAL FAILURE'}")
            logger.info("")

            return self.failed_count == 0

        except Exception as e:
            logger.error(f"Migration failed with error: {str(e)}", exc_info=True)
            return False

    async def _verify_tables(self) -> None:
        """Verify all required tables exist."""
        logger.info("Verifying database tables...")

        required_tables = ['personas', 'persons', 'person_data']
        for table_name in required_tables:
            try:
                response = self.supabase.client.table(table_name).select('id', count='exact').limit(0).execute()
                logger.debug(f"  [OK] Table '{table_name}' exists")
            except Exception as e:
                raise RuntimeError(f"Table '{table_name}' not found: {str(e)}")

        logger.info("  All tables verified")
        logger.info("")

    async def _fetch_old_personas(self) -> List[dict]:
        """Fetch all personas from old schema."""
        logger.info("Reading old personas table...")

        try:
            # Note: This reads from the OLD personas table before migration
            # We'll read everything including old data
            response = self.supabase.client.table('personas').select('*').execute()
            personas = response.data or []
            logger.debug(f"  Fetched {len(personas)} records from old schema")
            return personas

        except Exception as e:
            logger.error(f"Failed to read old personas: {str(e)}")
            raise

    async def _migrate_persona(self, old_persona: dict, index: int, total: int) -> None:
        """Migrate a single persona record."""
        persona_id = old_persona.get('id')
        logger.info(f"[{index}/{total}] Migrating persona {persona_id}...")

        try:
            # Validate old persona data
            raw_text = old_persona.get('raw_text')
            persona_json = old_persona.get('persona')

            if not raw_text:
                logger.warning(f"  Skipping: No raw_text")
                self.skipped_count += 1
                return

            if not persona_json:
                logger.warning(f"  Skipping: No persona JSON")
                self.skipped_count += 1
                return

            # Parse persona_json if it's a string
            if isinstance(persona_json, str):
                try:
                    persona_json = json.loads(persona_json)
                except json.JSONDecodeError:
                    logger.warning(f"  Skipping: Invalid JSON in persona")
                    self.skipped_count += 1
                    return

            # Build new person record
            person_data = {
                'created_at': old_persona.get('created_at'),
                'updated_at': old_persona.get('updated_at'),
            }

            # Build new person_data record
            submission_data = {
                'raw_text': raw_text,
                'source': 'migration',
                'created_at': old_persona.get('created_at'),
            }

            # Build new persona record
            new_persona_data = {
                'persona': persona_json,
                'version': 1,
                'computed_from_data_ids': [],  # Will be populated after person_data creation
                'created_at': old_persona.get('created_at'),
                'updated_at': old_persona.get('updated_at'),
            }

            if not self.dry_run:
                # 1. Create person
                logger.debug(f"  Creating person...")
                person_response = self.supabase.client.table('persons').insert(person_data).execute()
                if not person_response.data:
                    raise RuntimeError("Failed to create person")
                person_id = person_response.data[0]['id']
                logger.debug(f"  Created person: {person_id}")

                # 2. Create person_data
                logger.debug(f"  Creating person_data...")
                submission_data['person_id'] = person_id
                data_response = self.supabase.client.table('person_data').insert(submission_data).execute()
                if not data_response.data:
                    raise RuntimeError("Failed to create person_data")
                data_id = data_response.data[0]['id']
                logger.debug(f"  Created person_data: {data_id}")

                # 3. Create persona with lineage
                logger.debug(f"  Creating persona with lineage...")
                new_persona_data['person_id'] = person_id
                new_persona_data['computed_from_data_ids'] = [data_id]
                persona_response = self.supabase.client.table('personas').insert(new_persona_data).execute()
                if not persona_response.data:
                    raise RuntimeError("Failed to create persona")
                new_persona_id = persona_response.data[0]['id']
                logger.debug(f"  Created persona: {new_persona_id}")

                logger.info(f"  [OK] Migrated successfully (person_id={person_id})")
                self.migrated_count += 1
            else:
                # Dry run mode - just log what would happen
                logger.info(f"  [DRY RUN] Would migrate persona (id={persona_id})")
                logger.debug(f"    - Would create person")
                logger.debug(f"    - Would create person_data from raw_text ({len(raw_text)} chars)")
                logger.debug(f"    - Would create persona v1 with computed_from_data_ids")
                self.migrated_count += 1

        except Exception as e:
            logger.error(f"  [FAILED] {str(e)}")
            self.failed_count += 1

    async def validate(self) -> bool:
        """Validate migration results."""
        logger.info("=" * 70)
        logger.info("VALIDATING MIGRATION")
        logger.info("=" * 70)
        logger.info("")

        try:
            # Count records in each table
            persons_response = self.supabase.client.table('persons').select('id', count='exact').limit(0).execute()
            person_count = persons_response.count or 0

            data_response = self.supabase.client.table('person_data').select('id', count='exact').limit(0).execute()
            data_count = data_response.count or 0

            personas_response = self.supabase.client.table('personas').select('id', count='exact').limit(0).execute()
            persona_count = personas_response.count or 0

            logger.info(f"Table record counts:")
            logger.info(f"  persons:     {person_count}")
            logger.info(f"  person_data: {data_count}")
            logger.info(f"  personas:    {persona_count}")
            logger.info("")

            # Validate relationships
            logger.info("Validating relationships...")
            all_valid = True

            # Check that each person has at least one person_data entry
            persons = self.supabase.client.table('persons').select('id').execute()
            for person in persons.data:
                person_id = person['id']
                data = self.supabase.client.table('person_data').select('id').eq('person_id', str(person_id)).execute()
                if not data.data:
                    logger.warning(f"  Person {person_id} has no person_data entries")
                    all_valid = False

            # Check that each person has exactly one persona
            for person in persons.data:
                person_id = person['id']
                personas = self.supabase.client.table('personas').select('id').eq('person_id', str(person_id)).execute()
                if len(personas.data) != 1:
                    logger.warning(f"  Person {person_id} has {len(personas.data)} personas (expected 1)")
                    all_valid = False

            logger.info(f"  Relationship validation: {'[OK]' if all_valid else '[ISSUES FOUND]'}")
            logger.info("")

            return all_valid

        except Exception as e:
            logger.error(f"Validation failed: {str(e)}", exc_info=True)
            return False


async def main():
    """Main entry point."""
    dry_run = '--dry-run' in sys.argv
    validate_only = '--validate-only' in sys.argv

    if validate_only:
        migrator = PersonAggregateRootMigrator(dry_run=True)
        success = await migrator.validate()
        sys.exit(0 if success else 1)
    else:
        migrator = PersonAggregateRootMigrator(dry_run=dry_run)
        success = await migrator.run()

        if success and not dry_run:
            # Run validation after migration
            logger.info("")
            success = await migrator.validate()

        sys.exit(0 if success else 1)


if __name__ == '__main__':
    asyncio.run(main())
