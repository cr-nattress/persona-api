# US-09-06: Implement Persona Recomputation Service Logic

**Epic**: EPIC-09

**User Story**: As a service developer, I want to implement the `recompute_persona()` method, so that personas are automatically regenerated from all accumulated data when new submissions arrive.

**Story Points**: 8

**Priority**: 🔴 Critical

## Acceptance Criteria

- [ ] `recompute_persona()` fetches all person_data in chronological order
- [ ] Raw text concatenated with separators ("---")
- [ ] LLM generates new persona from accumulated text
- [ ] Version number incremented correctly
- [ ] computed_from_data_ids array properly tracked
- [ ] Handles case when no data exists (returns None)
- [ ] Handles LLM failures gracefully
- [ ] Integration tests pass

## Workflow

1. Fetch all person_data for person (order by created_at ASC)
2. If no data: return None
3. Concatenate raw_text with separators
4. Call LLM chain to generate persona
5. Get current persona (if exists) to get version
6. Increment version (or set to 1 if first)
7. Collect all person_data IDs
8. Update/create personas record with new version, JSON, and IDs
9. Return updated persona

## Task List

1. TASK-09-06-01: Implement recompute_persona() method
2. TASK-09-06-02: Add text concatenation and accumulation
3. TASK-09-06-03: Implement version incrementing
4. TASK-09-06-04: Add error handling for LLM failures
5. TASK-09-06-05: Write integration tests

---

**Story Points**: 8 | **Time**: 3-4 hours | **Depends on**: US-09-03, US-09-04, US-09-05
