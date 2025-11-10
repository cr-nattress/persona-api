-- Migration: 002_create_person_aggregate_schema.sql
-- Purpose: Create person aggregate root schema with unstructured data history
-- Description: Implements the person aggregate root pattern with proper versioning
--              and data lineage tracking for personas
-- Date: 2025-11-09

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- PERSONS TABLE - Aggregate Root
-- ============================================================================
-- Purpose: Root entity for person aggregate. Minimal data, links to all
--          person-related records (data submissions and computed personas).
-- ============================================================================

CREATE TABLE IF NOT EXISTS public.persons (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name VARCHAR(255) NULL,
    last_name VARCHAR(255) NULL,
    gender VARCHAR(50) NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.persons IS 'Person aggregate root. Represents a unique individual with related data and personas.';
COMMENT ON COLUMN public.persons.id IS 'Unique identifier (UUID v4)';
COMMENT ON COLUMN public.persons.first_name IS 'First name of the person (optional)';
COMMENT ON COLUMN public.persons.last_name IS 'Last name of the person (optional)';
COMMENT ON COLUMN public.persons.gender IS 'Gender of the person: male, female, other, prefer not to say (optional)';
COMMENT ON COLUMN public.persons.created_at IS 'Timestamp when person record created';
COMMENT ON COLUMN public.persons.updated_at IS 'Timestamp when person record last updated';

-- Create trigger for updating person timestamps
CREATE OR REPLACE FUNCTION update_persons_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_persons_updated_at ON public.persons;

CREATE TRIGGER trigger_persons_updated_at
BEFORE UPDATE ON public.persons
FOR EACH ROW
EXECUTE FUNCTION update_persons_updated_at();

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
    source TEXT DEFAULT 'api',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_person_data_person FOREIGN KEY (person_id)
        REFERENCES public.persons(id) ON DELETE CASCADE
);

COMMENT ON TABLE public.person_data IS 'Unstructured data submission history. One row per API call. Complete history of all data sent for a person.';
COMMENT ON COLUMN public.person_data.id IS 'Unique identifier for this data submission';
COMMENT ON COLUMN public.person_data.person_id IS 'Foreign key to persons table (aggregate root)';
COMMENT ON COLUMN public.person_data.raw_text IS 'Complete unstructured text submitted in this API call';
COMMENT ON COLUMN public.person_data.source IS 'Source of data (api, urls, import, etc). Defaults to api.';
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
--
-- NOTE: The existing personas table schema will be replaced by this new
--       structure. Data migration will be handled in a separate migration
--       (see US-09-13: Data Migration Script).
-- ============================================================================

-- Drop the old personas table if it exists and recreate with new schema
DROP TABLE IF EXISTS public.personas CASCADE;

CREATE TABLE IF NOT EXISTS public.personas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id UUID NOT NULL UNIQUE,
    persona JSONB NOT NULL,
    computed_from_data_ids UUID[] NOT NULL DEFAULT '{}',
    version INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_personas_person FOREIGN KEY (person_id)
        REFERENCES public.persons(id) ON DELETE CASCADE
);

COMMENT ON TABLE public.personas IS 'Current/latest computed persona for a person. Tracks version and data lineage.';
COMMENT ON COLUMN public.personas.id IS 'Unique identifier for this persona record';
COMMENT ON COLUMN public.personas.person_id IS 'Foreign key to persons table (UNIQUE - one persona per person)';
COMMENT ON COLUMN public.personas.persona IS 'JSONB containing computed persona structure and attributes';
COMMENT ON COLUMN public.personas.computed_from_data_ids IS 'UUID array of person_data IDs used in this computation (lineage tracking)';
COMMENT ON COLUMN public.personas.version IS 'Version number (increments with each recomputation). Starts at 1.';
COMMENT ON COLUMN public.personas.created_at IS 'When persona first computed for this person';
COMMENT ON COLUMN public.personas.updated_at IS 'When persona last recomputed';

-- Create indexes for query performance
CREATE INDEX IF NOT EXISTS idx_personas_person_id
    ON public.personas(person_id);

CREATE INDEX IF NOT EXISTS idx_personas_updated_at
    ON public.personas(updated_at DESC);

CREATE INDEX IF NOT EXISTS idx_personas_version
    ON public.personas(version);

-- Create trigger for updating persona timestamps
CREATE OR REPLACE FUNCTION update_personas_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_personas_updated_at ON public.personas;

CREATE TRIGGER trigger_personas_updated_at
BEFORE UPDATE ON public.personas
FOR EACH ROW
EXECUTE FUNCTION update_personas_updated_at();

-- ============================================================================
-- Migration complete
-- ============================================================================
-- Summary of changes:
--   1. Created persons table (aggregate root)
--   2. Created person_data table (unstructured data history)
--   3. Replaced personas table with new schema (version tracking, lineage)
--
-- Next steps (in separate migration US-09-13):
--   - Run data migration script to convert existing personas
--   - Populate person_data and new personas schema from legacy data
-- ============================================================================
