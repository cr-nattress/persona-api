#!/usr/bin/env python3
"""
Run database migrations against Supabase.

This script reads migration files and applies them to the Supabase database.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()


class MigrationRunner:
    """Run database migrations."""

    def __init__(self, supabase_url: str, supabase_key: str):
        """Initialize with Supabase credentials."""
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self.connection = None

    def parse_connection_string(self) -> dict:
        """
        Parse Supabase URL to extract connection details.

        Supabase uses PostgreSQL and provides a connection string.
        We'll use the REST API approach instead.
        """
        # Extract project reference from URL
        # URL format: https://xxxxx.supabase.co
        match = re.search(r'https://([^.]+)\.supabase\.co', self.supabase_url)
        if not match:
            raise ValueError(f"Invalid Supabase URL: {self.supabase_url}")

        project_ref = match.group(1)

        # Supabase provides PostgreSQL connection details
        # We'll construct the connection string
        return {
            'project_ref': project_ref,
            'api_key': self.supabase_key,
            'url': self.supabase_url,
        }

    def connect(self) -> bool:
        """Prepare Supabase connection."""
        print("Supabase project configured from environment variables")
        print("Ready to apply migration through Supabase dashboard")
        print()
        return True

    def load_migration(self, migration_file: str) -> str:
        """Load migration SQL from file."""
        migration_path = Path(__file__).parent / migration_file
        if not migration_path.exists():
            raise FileNotFoundError(f"Migration file not found: {migration_path}")

        with open(migration_path, 'r') as f:
            return f.read()

    def apply_migration_manual(self, sql_content: str) -> None:
        """
        Display instructions for manual migration application.

        Since we don't have the Service Role Key for direct access,
        users should apply migrations through Supabase dashboard.
        """
        print("=" * 70)
        print("MANUAL MIGRATION INSTRUCTIONS")
        print("=" * 70)
        print()
        print("Migration File: db/migrations/002_create_person_aggregate_schema.sql")
        print()
        print("To apply this migration:")
        print()
        print("1. Open Supabase Dashboard:")
        print("   https://app.supabase.com")
        print()
        print("2. Select your project")
        print()
        print("3. Navigate to SQL Editor")
        print()
        print("4. Create a new query")
        print()
        print("5. Copy this SQL and paste into the editor:")
        print()
        print("-" * 70)
        print(sql_content)
        print("-" * 70)
        print()
        print("6. Click 'Run'")
        print()
        print("7. Verify success:")
        print("   - Check for 'All good!' message")
        print("   - No error messages should appear")
        print()
        print("=" * 70)


def main():
    """Main entry point."""
    # Get credentials from environment
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not supabase_url or not supabase_key:
        print("Error: SUPABASE_URL and SUPABASE_ANON_KEY not set in .env")
        return 1

    # Create runner
    runner = MigrationRunner(supabase_url, supabase_key)

    # Load migration
    try:
        migration_sql = runner.load_migration("migrations/002_create_person_aggregate_schema.sql")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1

    # Connect
    runner.connect()

    # Check if we have service role key for direct connection
    if service_role_key:
        print("[INFO] Service Role Key found. Direct database connection available.")
        print("[INFO] To implement direct migration, configure database connection details.")
    else:
        print("[INFO] Service Role Key not set. Using manual application method.")
        print()

    # Apply migration
    runner.apply_migration_manual(migration_sql)

    return 0


if __name__ == "__main__":
    sys.exit(main())
