# US-09-07: Implement Person CRUD Service Methods

**Epic**: EPIC-09 | **Points**: 5 | **Priority**: 🔴 Critical

## User Story

As a service developer, I want to implement person lifecycle methods in PersonService, so that we have high-level operations for creating, reading, updating, and deleting persons.

## Acceptance Criteria

- [ ] `create_person()` creates new person aggregate root
- [ ] `get_person()` retrieves person with metadata
- [ ] `list_persons()` with pagination
- [ ] `delete_person()` cascades to related data
- [ ] All methods use PersonRepository
- [ ] Error handling for non-existent records
- [ ] Unit tests pass

## Task List

1. TASK-09-07-01: Add person lifecycle methods to PersonService
2. TASK-09-07-02: Implement error handling
3. TASK-09-07-03: Write unit tests

---

**Time**: 2-3 hours | **Depends on**: US-09-03
