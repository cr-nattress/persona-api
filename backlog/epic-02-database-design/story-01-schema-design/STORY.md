# US-02-01: Design Personas Table Schema

**Epic:** EPIC-02: Database Design & Supabase Integration

**User Story:** As a database architect, I want a well-designed schema for storing persona data, so that queries are efficient and data integrity is maintained.

**Story Points:** 5

**Priority:** 🔴 Critical (High)

## Acceptance Criteria
- [ ] Personas table schema designed with UUID primary key
- [ ] JSONB column for flexible persona data
- [ ] Timestamp columns for audit trail
- [ ] Proper indexes created for performance
- [ ] SQL script verified and executable
- [ ] Schema documentation created

## Definition of Done
- [ ] SQL migration script created and tested
- [ ] Schema documentation updated
- [ ] Indexes defined and verified

## Technical Notes

**Schema Design:**
```sql
CREATE TABLE personas (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  raw_text TEXT NOT NULL,
  persona JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_personas_created_at ON personas(created_at DESC);
CREATE INDEX idx_personas_updated_at ON personas(updated_at DESC);
```

## Tasks
- TASK-02-01-01: Design schema and create migration
- TASK-02-01-02: Create indexes for performance
- TASK-02-01-03: Add RLS policies for security

---

**Story Points:** 5 | **Priority:** High | **Target Sprint:** Sprint 1
