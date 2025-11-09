# US-09-08: Implement Data Accumulation Service Methods

**Epic**: EPIC-09 | **Points**: 5 | **Priority**: 🔴 Critical

## User Story

As a service developer, I want to implement methods for adding data and triggering persona recomputation, so that new submissions automatically accumulate and improve personas.

## Acceptance Criteria

- [ ] `add_person_data()` creates new person_data row
- [ ] `add_person_data_and_regenerate()` atomically adds data + recomputes
- [ ] `get_person_data_history()` retrieves paginated history
- [ ] Recomputation triggered after each data addition
- [ ] Transaction handling for atomic operations
- [ ] Error handling for invalid persons
- [ ] Unit tests pass

## Task List

1. TASK-09-08-01: Add data management methods to PersonService
2. TASK-09-08-02: Implement atomic add-and-regenerate
3. TASK-09-08-03: Write unit tests

---

**Time**: 2-3 hours | **Depends on**: US-09-04, US-09-06, US-09-07
