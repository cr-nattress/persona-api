# EPIC-09: Person Aggregate Root with Unstructured Data History

**Status:** 📋 Ready | **Points:** 117 | **Priority:** 🔴 Critical

## Business Value

Redesign the core data model to properly support **incremental persona improvement**. Currently, each PATCH overwrites the previous persona. With this epic, we implement a person aggregate root that accumulates unstructured data across multiple API calls, automatically recomputing personas based on ALL accumulated historical data.

### Key Benefits

- **Data Lineage & Audit Trail**: Know exactly which data generated which persona version
- **Incremental Learning**: Each API call adds context; personas improve over time without data loss
- **Proper History Preservation**: Complete submission history for retraining and debugging
- **Better LLM Context**: Recomputation uses ALL accumulated context, not just latest data
- **Backward Compatible**: Existing clients continue to work through adapter endpoints

## Current State

- Single `personas` table with `id`, `raw_text`, `persona`, `created_at`, `updated_at`
- PATCH endpoint overwrites both `raw_text` and `persona` fields
- No history of individual submissions preserved
- No versioning or lineage tracking
- Personas are independent entities, not tied to a "person"

## Target State

- Three-table design with proper aggregate root pattern:
  - `persons`: Root aggregate (id, timestamps)
  - `person_data`: History of all unstructured submissions (id, person_id, raw_text, created_at)
  - `personas`: Current computed persona (id, person_id, persona, version, computed_from_data_ids)
- Each PATCH adds row to `person_data`, triggers persona recomputation
- Personas track version numbers and which data IDs they were computed from
- New API endpoints for person management and data history retrieval
- Backward-compatible wrappers maintain existing `/v1/persona/*` endpoint support

## Technical Approach

### Database Schema
1. Create `persons` table (aggregate root)
2. Create `person_data` table (unstructured data history) with FK to persons
3. Redesign `personas` table (add person_id, version, computed_from_data_ids)
4. Add indexes on person_id and created_at for query performance
5. Create migration script to convert existing personas

### Data Models (Python)
1. Define Person models (base, create, response)
2. Define PersonData models (base, create, response)
3. Update Persona models (add person_id, version, computed_from_data_ids)
4. Add validation and constraints

### Repository Layer
1. Create PersonRepository (CRUD for persons)
2. Create PersonDataRepository (store and retrieve submissions)
3. Update PersonaRepository (handle versioning and lineage)

### Service Layer & Business Logic
1. Implement `recompute_persona()` method:
   - Fetch all person_data records (ordered by created_at)
   - Concatenate all raw_text with separators
   - Call LLM to generate persona from accumulated text
   - Increment version, track data IDs
2. Implement person CRUD methods in PersonService
3. Add data accumulation and atomic operations

### API Endpoints (New)
1. `POST /v1/person` - Create new person aggregate root
2. `POST /v1/person/{person_id}/data` - Add unstructured data
3. `POST /v1/person/{person_id}/data-and-regenerate` - Add data + regenerate atomically
4. `GET /v1/person/{person_id}` - Get person metadata
5. `GET /v1/person/{person_id}/data` - List accumulated data with pagination
6. `GET /v1/person/{person_id}/persona` - Get current persona
7. `GET /v1/person/{person_id}/persona-with-history` - Get persona with source data

### Backward Compatibility
- Implement adapter endpoints under `/v1/persona/*` that map to new person endpoints
- Support legacy behavior where needed
- Gradual migration path for existing clients

## Acceptance Criteria

- [ ] All three new tables created and indexed
- [ ] All Python data models defined with validation
- [ ] All repository methods implemented
- [ ] Persona recomputation logic working correctly
- [ ] All 7 new API endpoints implemented
- [ ] Backward-compatible endpoints working
- [ ] Data migration script converts existing personas without loss
- [ ] Integration tests pass with 80%+ code coverage
- [ ] No regressions in existing persona endpoints
- [ ] API documentation updated with new endpoints

## User Stories

1. **US-09-01**: Create Database Schema (persons, person_data, personas tables)
2. **US-09-02**: Create Python Data Models (Person, PersonData, updated Persona)
3. **US-09-03**: Implement Person Repository Layer
4. **US-09-04**: Implement PersonData Repository Layer
5. **US-09-05**: Update Persona Repository with Versioning
6. **US-09-06**: Implement Persona Recomputation Service Logic
7. **US-09-07**: Implement Person CRUD Service Methods
8. **US-09-08**: Implement Data Accumulation Service Methods
9. **US-09-09**: Create Person Management API Endpoints
10. **US-09-10**: Create Data History API Endpoints
11. **US-09-11**: Create Persona Retrieval API Endpoints
12. **US-09-12**: Implement Backward-Compatible Adapter Endpoints
13. **US-09-13**: Create Data Migration Script
14. **US-09-14**: Write Integration Tests
15. **US-09-15**: Create Deployment & Migration Guide

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **Data migration errors** | Could lose existing data | Run migration on backup first; verify row counts; log transformation |
| **Breaking existing clients** | Service outage for existing users | Maintain backward-compatible endpoints; gradual migration |
| **LLM context too long** | Token limit exceeded | Implement text chunking; track token count; fail gracefully |
| **Performance regression** | Slow persona recomputation | Profile queries; add indexes; optimize concatenation |
| **FK constraint issues** | Migration fails | Test constraints on small dataset first; handle orphaned records |

## Success Metrics

- All 117 story points completed
- Zero data loss during migration
- All existing personas successfully converted
- New endpoints operational and tested
- Integration tests pass
- No performance regression in read operations
- Backward-compatible endpoints functional
- Documentation complete and accurate

## Estimated Effort

| Phase | Stories | Points | Weeks |
|-------|---------|--------|-------|
| **Phase 1: Database & Models** | Stories 1-2 | 18 | 1.5 |
| **Phase 2: Repositories** | Stories 3-5 | 21 | 1.5 |
| **Phase 3: Service Logic** | Stories 6-8 | 24 | 2 |
| **Phase 4: API Endpoints** | Stories 9-12 | 28 | 2.5 |
| **Phase 5: Testing & Migration** | Stories 13-15 | 26 | 2 |
| **Total** | **15** | **117** | **9.5 weeks** |

## Dependencies

- **Blocked by**: EPIC-02 (Database Design), EPIC-03 (Repository Pattern)
- **Blocks**: Any client code relying on person/data history features
- **Related**: EPIC-05 (Service Layer), EPIC-04 (API Endpoints)

## Recommended Team

- **1 Backend Developer**: Database schema + repositories
- **1 Service Developer**: Business logic + persona recomputation
- **1 API Developer**: Endpoints + backward compatibility

Can be completed with 2 developers (sequential phases) or 1 developer over 9-10 weeks solo.

## Phase Breakdown

### Phase 1: Foundation (Weeks 1-1.5)
**Epics**: US-09-01 (Database)
- Create migration SQL with three tables
- Test migration on local database
- Verify schema with indexes

### Phase 2: Models & Repos (Weeks 1.5-3)
**Epics**: US-09-02 through US-09-05
- Define all Python models
- Implement all repository CRUD methods
- Unit test repositories

### Phase 3: Service Logic (Weeks 3-5)
**Epics**: US-09-06 through US-09-08
- Implement persona recomputation
- Implement person lifecycle methods
- Implement data accumulation
- Unit test service layer

### Phase 4: API (Weeks 5-7.5)
**Epics**: US-09-09 through US-09-12
- Create all 7 new endpoints
- Create backward-compatible wrappers
- Integration test endpoints

### Phase 5: Polish & Deploy (Weeks 7.5-9.5)
**Epics**: US-09-13 through US-09-15
- Create and test data migration script
- Write integration tests (80%+ coverage)
- Create deployment guide
- Test on staging environment

---

**Next Steps:**
1. Review IMPLEMENTATION-PLAN.md for architectural details
2. Start with story US-09-01: Create Database Schema
3. Follow stories in order (dependencies are sequential until Phase 3)
