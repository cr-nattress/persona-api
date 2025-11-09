# US-09-02: Create Python Data Models (Person, PersonData, Updated Persona)

**Epic**: EPIC-09

**User Story**: As a backend developer, I want to define all Python data models for the new schema, so that we have type-safe, validated representations of persons, person_data, and personas.

**Story Points**: 8

**Priority**: 🔴 Critical

## Acceptance Criteria

- [ ] Person models created (PersonBase, PersonCreate, PersonInDB, PersonResponse)
- [ ] PersonData models created with all variants
- [ ] Persona models updated with version and computed_from_data_ids
- [ ] All models include docstrings and field descriptions
- [ ] Validation rules implemented (UUID format, string lengths, etc.)
- [ ] Response models use separate types from internal models
- [ ] Models follow existing codebase patterns
- [ ] Unit tests for model validation pass

## Technical Notes

### New Models to Create

**Person Models**
```python
class PersonBase(BaseModel): pass
class PersonCreate(BaseModel): pass
class PersonInDB(PersonBase): id, created_at, updated_at
class PersonResponse(PersonInDB): person_data_count, latest_persona_version
```

**PersonData Models**
```python
class PersonDataBase(BaseModel): raw_text, source
class PersonDataCreate(PersonDataBase): person_id
class PersonDataInDB(PersonDataBase): id, person_id, created_at
class PersonDataResponse(PersonDataInDB): pass
```

**Updated Persona Models**
```python
class PersonaBase(BaseModel): persona (dict)
class PersonaInDB(PersonaBase): id, person_id, version, computed_from_data_ids
class PersonaResponse(PersonaInDB): pass
class PersonaWithHistory(PersonaResponse): computed_from_data (list[PersonDataResponse])
```

### Location

Create/update in `app/models/`:
- `person.py` (NEW)
- `person_data.py` (NEW)
- `persona.py` (UPDATED)

## Definition of Done

- [ ] All model files created with proper structure
- [ ] All fields have Pydantic validators where needed
- [ ] Models follow existing codebase conventions
- [ ] Docstrings explain purpose of each model
- [ ] Tests verify model validation works
- [ ] Import statements in `__init__.py` updated
- [ ] Commit: `feat(models): add person aggregate root models`

## Task List

1. TASK-09-02-01: Create Person models (PersonBase, PersonCreate, PersonInDB, PersonResponse)
2. TASK-09-02-02: Create PersonData models (PersonDataBase, PersonDataCreate, PersonDataInDB, Response)
3. TASK-09-02-03: Update Persona models with version and computed_from_data_ids
4. TASK-09-02-04: Add validation and update model imports
5. TASK-09-02-05: Write unit tests for model validation

---

**Estimated Time**: 3-4 hours

**Dependencies**: Story US-09-01 complete

**Blocks**: Stories US-09-03 through US-09-08
