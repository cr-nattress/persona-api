# US-09-03: Implement Person Repository Layer

**Epic**: EPIC-09

**User Story**: As a backend developer, I want to implement the PersonRepository with full CRUD operations, so that we have a clean data access layer for person records.

**Story Points**: 5

**Priority**: 🔴 Critical

## Acceptance Criteria

- [ ] PersonRepository class created with async CRUD methods
- [ ] `create()` method creates new person and returns PersonInDB
- [ ] `read()` method retrieves person by ID
- [ ] `read_all()` method with pagination support
- [ ] `update()` method updates person
- [ ] `delete()` method deletes person (cascades to related data)
- [ ] Error handling for FK violations and non-existent records
- [ ] Unit tests for all methods pass
- [ ] Repository follows existing patterns (see PersonaRepository)

## Task List

1. TASK-09-03-01: Create PersonRepository class and async methods
2. TASK-09-03-02: Implement CRUD operations with error handling
3. TASK-09-03-03: Add pagination support to read_all()
4. TASK-09-03-04: Write unit tests for PersonRepository

---

**Estimated Time**: 2-3 hours | **Depends on**: US-09-01, US-09-02 | **Blocks**: US-09-06
