# US-09-05: Update Persona Repository with Versioning

**Epic**: EPIC-09

**User Story**: As a backend developer, I want to update PersonaRepository to handle persona versioning and track which data IDs were used in computation, so that we have proper lineage tracking.

**Story Points**: 5

**Priority**: 🔴 Critical

## Acceptance Criteria

- [ ] PersonaRepository updated for new schema (person_id, version, computed_from_data_ids)
- [ ] `get_by_person_id()` method retrieves current persona for a person
- [ ] `update_by_person_id()` increments version and updates lineage
- [ ] `upsert()` creates or updates persona atomically
- [ ] Version tracking works correctly (1, 2, 3...)
- [ ] UUID array storage verified
- [ ] Unit tests pass

## Task List

1. TASK-09-05-01: Update PersonaRepository for new schema
2. TASK-09-05-02: Implement version and lineage tracking
3. TASK-09-05-03: Add upsert logic
4. TASK-09-05-04: Write unit tests

---

**Story Points**: 5 | **Time**: 2-3 hours | **Depends on**: US-09-02
