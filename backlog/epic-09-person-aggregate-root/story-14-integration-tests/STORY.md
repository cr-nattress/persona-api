# US-09-14: Write Comprehensive Integration Tests

**Epic**: EPIC-09 | **Points**: 10 | **Priority**: 🔴 Critical

## User Story

As a QA engineer, I want to create comprehensive integration tests for the entire person aggregate root feature, so that we can verify end-to-end functionality and prevent regressions.

## Acceptance Criteria

- [ ] Integration tests cover all new endpoints
- [ ] Tests verify data accumulation workflow
- [ ] Tests verify persona recomputation
- [ ] Tests verify versioning and lineage
- [ ] Tests verify backward compatibility
- [ ] Tests verify data integrity (cascade deletes, FK constraints)
- [ ] 80%+ code coverage achieved
- [ ] All tests pass
- [ ] Performance acceptable (persona recomputation < 5s)

## Test Scenarios

1. Create person → verify created
2. Add data → verify stored
3. Retrieve person → verify with metadata
4. Add data → recompute persona → verify version 2
5. Add more data → recompute → verify version 3
6. Retrieve history → verify all data
7. Retrieve with history → verify lineage
8. Delete person → verify cascades
9. Backward-compatible PATCH → verify works

## Task List

1. TASK-09-14-01: Set up test fixtures and helpers
2. TASK-09-14-02: Write endpoint integration tests
3. TASK-09-14-03: Write recomputation workflow tests
4. TASK-09-14-04: Write backward-compatibility tests
5. TASK-09-14-05: Verify code coverage and performance

---

**Time**: 3-4 hours | **Depends on**: All previous stories
