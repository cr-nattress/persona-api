# Implementation Plan: Person Aggregate Root with Unstructured Data History

## Overview
Redesign the database schema to support a person aggregate root that accumulates unstructured data across multiple API calls, with automatic persona recomputation based on all accumulated data.

## Key Requirements
1. Create person aggregate root as the central entity
2. Store complete history of unstructured data submissions (one row per API call)
3. Automatically recompute persona by concatenating all accumulated data and regenerating via LLM
4. Track persona versions and which person_data records generated each persona
5. Maintain backward compatibility with existing API

## Database Schema Design

### New Tables Structure

#### Table 1: `persons` (Aggregate Root)
```sql
CREATE TABLE public.persons (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

#### Table 2: `person_data` (Unstructured Data History)
```sql
CREATE TABLE public.person_data (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  person_id UUID NOT NULL REFERENCES persons(id) ON DELETE CASCADE,
  raw_text TEXT NOT NULL,
  source TEXT, -- optional: 'api', 'urls', etc.
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  CONSTRAINT fk_person_data_person FOREIGN KEY (person_id)
    REFERENCES persons(id) ON DELETE CASCADE
);

CREATE INDEX idx_person_data_person_id ON person_data(person_id);
CREATE INDEX idx_person_data_created_at ON person_data(created_at);
```

#### Table 3: `personas` (Current Persona - Computed Result)
```sql
CREATE TABLE public.personas (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  person_id UUID NOT NULL UNIQUE REFERENCES persons(id) ON DELETE CASCADE,
  persona JSONB NOT NULL,
  computed_from_data_ids UUID[] NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  CONSTRAINT fk_personas_person FOREIGN KEY (person_id)
    REFERENCES persons(id) ON DELETE CASCADE
);

CREATE INDEX idx_personas_person_id ON personas(person_id);
CREATE INDEX idx_personas_updated_at ON personas(updated_at);
```

## Data Model Changes (Python)

### New Models
- Person (aggregate root with basic metadata)
- PersonData (unstructured data submission record)
- Persona (computed result with version tracking)

### Updated Models
- PersonResponse with person_data_count and latest_persona_version
- PersonaInDB with person_id, version, and computed_from_data_ids

## API Contract Changes

### New Endpoints
- `POST /v1/person` - Create new person aggregate root
- `POST /v1/person/{person_id}/data` - Add unstructured data
- `POST /v1/person/{person_id}/data-and-regenerate` - Add data and regenerate persona atomically
- `GET /v1/person/{person_id}` - Get person with metadata
- `GET /v1/person/{person_id}/data` - List all accumulated data with pagination
- `GET /v1/person/{person_id}/persona` - Get current persona
- `GET /v1/person/{person_id}/persona-with-history` - Get persona with source data

### Updated Endpoints
- `PATCH /v1/person/{person_id}` - Create person and initial persona in one call

## Business Logic

### Persona Recomputation Workflow
1. Fetch ALL person_data records for person (ordered by created_at)
2. Concatenate all raw_text values in order with separators
3. Call LLM to generate new persona JSON from accumulated text
4. Increment persona version number
5. Update personas table with new version, data IDs, and JSON
6. Track which person_data IDs were used in computation

### Service Layer Methods
- `create_person()` - Create person aggregate root
- `add_person_data()` - Add data and trigger recomputation
- `add_person_data_and_regenerate()` - Atomic: add data + return updated persona
- `get_person_data_history()` - List accumulated data
- `get_current_persona()` - Get latest persona
- `recompute_persona()` - Internal recomputation logic

## Repository Layer

### New Repositories
- PersonRepository - CRUD for persons
- PersonDataRepository - Store and retrieve unstructured data

### Updated Repositories
- PersonaRepository - Handle versioning and tracking computed_from_data_ids

## Migration Strategy

### Database Migration
1. Create new tables (persons, person_data, personas)
2. Data migration script to convert existing personas
3. Add constraints and indexes

### Application Migration
1. Deploy new schema first
2. Deploy new code with backward-compatible endpoints
3. Gradual client migration to new endpoints
4. Deprecate old endpoints after adoption

## Benefits

- **Full History**: Every data submission preserved in person_data table
- **Audit Trail**: Know which data generated which persona version
- **Incremental Updates**: PATCH adds data without overwriting history
- **Proper Recomputation**: All accumulated context available for LLM
- **Data Integrity**: Foreign keys and cascade deletes
- **Flexible Schema**: JSONB for personas remains unchanged
- **Backward Compatible**: Old API can be maintained via wrappers
