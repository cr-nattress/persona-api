# TASK-09-01-01: Create Migration SQL File with Three Table Definitions

**Story**: US-09-01: Create Database Schema

**Estimated Time**: 45 minutes

**Description**: Create the complete SQL migration file that defines the three new tables (persons, person_data, personas) with all constraints, indexes, and comments. This is the foundation for the person aggregate root schema.

## Agent Prompt

You are implementing EPIC-09: Person Aggregate Root with Unstructured Data History.

**Goal**: Create a complete, production-ready SQL migration file that defines three new database tables with proper constraints, indexes, and documentation.

**Context**: We're redesigning the database to support incremental persona improvement. The new schema uses an aggregate root pattern with a persons table, a person_data table for unstructured data history, and a redesigned personas table with versioning.

**Instructions**:

1. **Locate the migrations directory**:
   - Check `db/migrations/` directory
   - Find the latest migration file to determine the next number
   - Current latest should be something like `001_create_personas_table.sql`
   - Create new file: `002_create_person_aggregate_schema.sql`

2. **Create the SQL migration with the following structure**:

```sql
-- Migration: 002_create_person_aggregate_schema.sql
-- Purpose: Create person aggregate root schema with unstructured data history
-- Date: 2025-11-09

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- PERSONS TABLE - Aggregate Root
-- ============================================================================
-- Purpose: Root entity for person aggregate. Minimal data, links to all
--          person-related records (data submissions and computed personas).
-- ============================================================================

CREATE TABLE IF NOT EXISTS public.persons (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_persons_id PRIMARY KEY (id)
);

COMMENT ON TABLE public.persons IS 'Person aggregate root. Represents a unique individual.';
COMMENT ON COLUMN public.persons.id IS 'Unique identifier (UUID)';
COMMENT ON COLUMN public.persons.created_at IS 'Timestamp when person record created';
COMMENT ON COLUMN public.persons.updated_at IS 'Timestamp when person record last updated';

-- ============================================================================
-- PERSON_DATA TABLE - Unstructured Data History
-- ============================================================================
-- Purpose: Store complete history of unstructured data submissions for a
--          person. Each row = one API call with all data sent in that call.
--          Ordered by created_at for sequential persona recomputation.
-- ============================================================================

CREATE TABLE IF NOT EXISTS public.person_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id UUID NOT NULL,
    raw_text TEXT NOT NULL,
    source TEXT DEFAULT 'api',  -- 'api', 'urls', 'import', etc.
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_person_data_person FOREIGN KEY (person_id)
        REFERENCES public.persons(id) ON DELETE CASCADE
);

COMMENT ON TABLE public.person_data IS 'Unstructured data submission history. One row per API call.';
COMMENT ON COLUMN public.person_data.id IS 'Unique identifier for this data submission';
COMMENT ON COLUMN public.person_data.person_id IS 'Foreign key to persons table';
COMMENT ON COLUMN public.person_data.raw_text IS 'Complete unstructured text submitted in this API call';
COMMENT ON COLUMN public.person_data.source IS 'Source of data (api, urls, import, etc)';
COMMENT ON COLUMN public.person_data.created_at IS 'When this data was submitted';

-- Create indexes for query performance
CREATE INDEX IF NOT EXISTS idx_person_data_person_id
    ON public.person_data(person_id);
CREATE INDEX IF NOT EXISTS idx_person_data_created_at
    ON public.person_data(created_at);

-- ============================================================================
-- PERSONAS TABLE - Current Computed Persona (Redesigned)
-- ============================================================================
-- Purpose: Store the current/latest computed persona for a person.
--          Replaces old single-table personas structure.
--          Tracks version and which data IDs were used in computation.
-- ============================================================================

CREATE TABLE IF NOT EXISTS public.personas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id UUID NOT NULL UNIQUE,
    persona JSONB NOT NULL,
    computed_from_data_ids UUID[] NOT NULL,  -- Array of person_data IDs used
    version INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_personas_person FOREIGN KEY (person_id)
        REFERENCES public.persons(id) ON DELETE CASCADE
);

COMMENT ON TABLE public.personas IS 'Current/latest computed persona for a person. Version tracked.';
COMMENT ON COLUMN public.personas.id IS 'Unique identifier for this persona record';
COMMENT ON COLUMN public.personas.person_id IS 'Foreign key to persons table (UNIQUE - one persona per person)';
COMMENT ON COLUMN public.personas.persona IS 'JSONB containing computed persona structure';
COMMENT ON COLUMN public.personas.computed_from_data_ids IS 'UUID array of person_data IDs used in this computation';
COMMENT ON COLUMN public.personas.version IS 'Version number (increments with each recomputation)';
COMMENT ON COLUMN public.personas.created_at IS 'When persona first computed';
COMMENT ON COLUMN public.personas.updated_at IS 'When persona last recomputed';

-- Create indexes for query performance
CREATE INDEX IF NOT EXISTS idx_personas_person_id
    ON public.personas(person_id);
CREATE INDEX IF NOT EXISTS idx_personas_updated_at
    ON public.personas(updated_at);

-- ============================================================================
-- Migration complete
-- ============================================================================
```

3. **Save the file** to `db/migrations/002_create_person_aggregate_schema.sql`

4. **Add helpful comments**:
   - Explain purpose of each table
   - Document each column
   - Explain the aggregate root pattern
   - Note the cascade delete behavior

5. **Verify the migration**:
   - Check for SQL syntax errors: no unclosed strings, proper keywords
   - Verify all table names match (persons, person_data, personas)
   - Ensure UUID extensions are enabled
   - Check all foreign key constraints are named
   - Verify indexes have descriptive names

## Verification Steps

1. **Read the migration file**:
   ```bash
   cat db/migrations/002_create_person_aggregate_schema.sql
   ```

2. **Check for syntax**:
   - All CREATE TABLE statements properly closed
   - All CONSTRAINT clauses include names
   - All INDEX definitions are correct
   - Comments are clear and descriptive

3. **Validate table names match**:
   - `persons` ✓
   - `person_data` ✓
   - `personas` ✓ (redesigned, not old personas)

4. **Verify foreign keys**:
   - person_data.person_id → persons.id (CASCADE DELETE)
   - personas.person_id → persons.id (CASCADE DELETE, UNIQUE)

5. **Check indexes exist**:
   - person_data(person_id)
   - person_data(created_at)
   - personas(person_id)
   - personas(updated_at)

## Expected Outcome

A complete, production-ready SQL migration file at `db/migrations/002_create_person_aggregate_schema.sql` that:
- Defines all three tables with proper structure
- Includes comprehensive comments
- Has all necessary constraints and indexes
- Is ready to be applied to the database
- Follows the existing migration pattern in the codebase

## File Location

**Create**: `db/migrations/002_create_person_aggregate_schema.sql`

## Estimated Time: 45 minutes

---

**Success Criteria**: Migration file is syntactically correct, complete, and ready for application.
