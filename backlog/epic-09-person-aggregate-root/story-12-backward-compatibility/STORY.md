# US-09-12: Implement Backward-Compatible Adapter Endpoints

**Epic**: EPIC-09 | **Points**: 8 | **Priority**: 🔴 Critical

## User Story

As an API developer, I want to implement adapter endpoints for existing `/v1/persona/*` routes, so that legacy clients continue to work without changes.

## Acceptance Criteria

- [ ] `PATCH /v1/persona/{person_id}` - Adapts to new person + data + regenerate flow
- [ ] Response matches old PersonaResponse format
- [ ] Backward-compatible behavior preserved
- [ ] No breaking changes for existing clients
- [ ] Integration tests verify compatibility
- [ ] Migration guide for clients created
- [ ] Swagger shows deprecation notices

## Implementation Notes

Map old endpoints to new:
- `PATCH /v1/persona/{id}` → Create person + add data + regenerate
- Return persona in legacy format

## Task List

1. TASK-09-12-01: Create backward-compatible endpoint adapters
2. TASK-09-12-02: Map old request/response formats to new
3. TASK-09-12-03: Write compatibility tests

---

**Time**: 2-3 hours | **Depends on**: US-09-09 through US-09-11
