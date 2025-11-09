# US-09-11: Create Persona Retrieval API Endpoints

**Epic**: EPIC-09 | **Points**: 5 | **Priority**: 🔴 Critical

## User Story

As an API developer, I want to create endpoints for retrieving current personas and their computation history, so that clients can access persona data with lineage information.

## Acceptance Criteria

- [ ] `GET /v1/person/{person_id}/persona` - Get current persona
- [ ] `GET /v1/person/{person_id}/persona-with-history` - Persona + source data
- [ ] Response includes version, computed_from_data_ids
- [ ] Persona JSON is complete and valid
- [ ] 404 if person or persona not found
- [ ] Integration tests pass
- [ ] Swagger documentation

## Task List

1. TASK-09-11-01: Create persona retrieval endpoints
2. TASK-09-11-02: Add history joining logic
3. TASK-09-11-03: Write integration tests

---

**Time**: 2-3 hours | **Depends on**: US-09-06
