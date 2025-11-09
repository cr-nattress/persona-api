# US-09-13: Create Data Migration Script for Existing Personas

**Epic**: EPIC-09 | **Points**: 8 | **Priority**: 🔴 Critical

## User Story

As a database engineer, I want to create a migration script that converts existing personas to the new schema, so that we don't lose any historical data during the transition.

## Acceptance Criteria

- [ ] Script reads all personas from old schema
- [ ] For each persona: creates person, person_data, new persona record
- [ ] raw_text stored in person_data table
- [ ] persona JSON stored in new personas table
- [ ] version set to 1 for all migrated personas
- [ ] computed_from_data_ids references single person_data record
- [ ] Row counts verified (before/after)
- [ ] No data loss
- [ ] Script tested on backup database
- [ ] Rollback capability documented

## Migration Logic

For each persona in old schema:
1. Create new person record
2. Create person_data record (raw_text)
3. Create personas record (version 1, computed_from_data_ids=[person_data_id])
4. Verify counts match

## Task List

1. TASK-09-13-01: Write Python migration script
2. TASK-09-13-02: Test migration on backup database
3. TASK-09-13-03: Verify data integrity
4. TASK-09-13-04: Document rollback procedures

---

**Time**: 2-3 hours | **Depends on**: US-09-01
