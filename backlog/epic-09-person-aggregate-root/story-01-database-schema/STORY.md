# US-09-01: Create Database Schema (Persons, Person Data, Personas Tables)

**Epic**: EPIC-09: Person Aggregate Root with Unstructured Data History

**User Story**: As a database engineer, I want to create the new three-table schema for person aggregates, so that we can properly track unstructured data history and persona versions.

**Story Points**: 8

**Priority**: 🔴 Critical

**Status**: 📋 Ready

## Acceptance Criteria

- [ ] `persons` table created with id (UUID PK), created_at, updated_at timestamps
- [ ] `person_data` table created with id, person_id (FK), raw_text, source, created_at
- [ ] `personas` table redesigned with id, person_id (FK, UNIQUE), persona (JSONB), version, computed_from_data_ids (UUID[])
- [ ] All foreign keys properly defined with ON DELETE CASCADE
- [ ] Indexes created on person_id and created_at for query performance
- [ ] Migration file generated and tested on local database
- [ ] Schema verified with pg_dump or similar
- [ ] No data loss during schema changes (tested)

## Technical Notes

### Schema Design

**persons table** (Aggregate Root)
- Minimal root entity
- Links all related data
- Auto-generated UUID PK
- Timestamps track creation and updates

**person_data table** (Unstructured Data History)
- One row per API submission
- Stores complete raw_text from that submission
- Foreign key to persons (CASCADE delete)
- Indexed on person_id and created_at for retrieval
- Source field optional (tracks origin: 'api', 'urls', etc)

**personas table** (Current Computed Persona)
- One row per person (UNIQUE constraint on person_id)
- Replaces old single `personas` table structure
- `version` tracks generation count (1, 2, 3...)
- `computed_from_data_ids` UUID[] array references exact person_data records used
- Maintains flexibility of JSONB for persona structure

### Migration Strategy

- New tables created alongside existing `personas` table
- Existing `personas` data will be migrated in separate story (US-09-13)
- Backward compatibility maintained during transition
- Rollback plan if needed

## Definition of Done

- [ ] SQL migration file created in `db/migrations/`
- [ ] Migration file follows naming convention: `00X_migrate_person_aggregate.sql`
- [ ] All CREATE TABLE statements include comments explaining purpose
- [ ] Foreign keys include constraint names (FK_person_data_person, etc)
- [ ] Indexes are explicitly named (idx_person_data_person_id, etc)
- [ ] Migration tested locally (applied and rolled back successfully)
- [ ] Schema validated: `SELECT * FROM information_schema.tables WHERE table_schema='public'`
- [ ] No syntax errors when running migration
- [ ] Commit with message: `feat(schema): create person aggregate root tables`

## Related Files

- `IMPLEMENTATION-PLAN.md` - Section 1: Database Schema Design
- `db/migrations/` - Existing migrations for reference
- `db/migrations/001_create_personas_table.sql` - Current schema to compare

## Task List

1. TASK-09-01-01: Create migration SQL file with three table definitions
2. TASK-09-01-02: Test migration locally
3. TASK-09-01-03: Verify schema with indexes and constraints
4. TASK-09-01-04: Create rollback script

---

## Estimated Time: 2-3 hours

**Complexity**: Medium (SQL schema creation + migration testing)

**Dependencies**: None (Foundation task)

**Blocks**: All other stories in this epic
