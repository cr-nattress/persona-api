# Person Aggregate Root Deployment Guide

Complete guide for deploying the Person Aggregate Root schema migration to production.

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Migration Strategy](#migration-strategy)
3. [Deployment Steps](#deployment-steps)
4. [Verification Steps](#verification-steps)
5. [Rollback Procedure](#rollback-procedure)
6. [Monitoring & Troubleshooting](#monitoring--troubleshooting)
7. [Data Lineage & Versioning](#data-lineage--versioning)

---

## Pre-Deployment Checklist

- [ ] Database backup created
- [ ] All integration tests passing
- [ ] Code reviewed and merged to main branch
- [ ] New environment variables configured (if any)
- [ ] Team notified of planned deployment
- [ ] Maintenance window scheduled
- [ ] Rollback procedure reviewed with team

### Database Backup

```bash
# Backup Supabase database
# Via Supabase Dashboard:
# 1. Go to Project > Database > Backups
# 2. Click "Create a backup"
# 3. Wait for backup to complete
```

### Code Status

```bash
# Verify all tests pass
pytest tests/test_person_aggregate_integration.py -v

# Verify no uncommitted changes
git status

# Verify deployment branch
git branch
```

---

## Migration Strategy

### Overview

The Person Aggregate Root migration transforms a flat personas table into a three-table aggregate root pattern:

**Before:**
```
personas
├── id (UUID)
├── raw_text (TEXT)
├── persona (JSONB)
├── created_at
└── updated_at
```

**After:**
```
persons (aggregate root)
├── id (UUID)
├── created_at
└── updated_at

person_data (immutable history)
├── id (UUID)
├── person_id (FK → persons)
├── raw_text (TEXT)
├── source (VARCHAR)
├── created_at
└── updated_at

personas (computed result)
├── id (UUID)
├── person_id (FK → persons, UNIQUE)
├── persona (JSONB)
├── version (INT)
├── computed_from_data_ids (UUID[])
├── created_at
└── updated_at
```

### Key Characteristics

- **Immutable History**: old persona records are never overwritten
- **Versioning**: each new computation increments version number
- **Lineage Tracking**: computed_from_data_ids tracks which submissions generated which persona
- **Cascade Delete**: deleting a person removes all related data and personas
- **No Data Loss**: migration maps old personas to new schema preserving all information

---

## Deployment Steps

### Phase 1: Schema Migration

#### Step 1.1: Apply Migration to Supabase

```bash
# 1. Open Supabase Dashboard
# 2. Go to Project > SQL Editor
# 3. Click "New Query"
# 4. Copy and paste the migration SQL:
```

**File**: `db/migrations/002_create_person_aggregate_schema.sql`

```sql
-- Create persons table (aggregate root)
CREATE TABLE IF NOT EXISTS public.persons (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create person_data table (immutable submission history)
CREATE TABLE IF NOT EXISTS public.person_data (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  person_id UUID NOT NULL REFERENCES public.persons(id) ON DELETE CASCADE,
  raw_text TEXT NOT NULL,
  source VARCHAR(50) DEFAULT 'api',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Add columns to existing personas table
ALTER TABLE public.personas
ADD COLUMN IF NOT EXISTS person_id UUID REFERENCES public.persons(id) ON DELETE CASCADE,
ADD COLUMN IF NOT EXISTS version INT DEFAULT 1,
ADD COLUMN IF NOT EXISTS computed_from_data_ids UUID[] DEFAULT ARRAY[]::UUID[];

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_persons_created_at ON public.persons(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_person_data_person_id ON public.person_data(person_id);
CREATE INDEX IF NOT EXISTS idx_person_data_created_at ON public.person_data(created_at);
CREATE INDEX IF NOT EXISTS idx_personas_person_id ON public.personas(person_id);
CREATE INDEX IF NOT EXISTS idx_personas_version ON public.personas(version);

-- Add unique constraint on person_id in personas (one persona per person)
ALTER TABLE public.personas ADD CONSTRAINT personas_person_id_unique UNIQUE (person_id);

-- Create triggers for timestamps
CREATE OR REPLACE FUNCTION update_persons_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_persons_updated_at ON public.persons;
CREATE TRIGGER trigger_persons_updated_at
BEFORE UPDATE ON public.persons
FOR EACH ROW
EXECUTE FUNCTION update_persons_updated_at();

-- Similar for person_data
CREATE OR REPLACE FUNCTION update_person_data_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_person_data_updated_at ON public.person_data;
CREATE TRIGGER trigger_person_data_updated_at
BEFORE UPDATE ON public.person_data
FOR EACH ROW
EXECUTE FUNCTION update_person_data_updated_at();
```

**Execution:**
```
4. Click "Run" button
5. Wait for query to complete
6. Verify no errors in output
7. Check tables exist: Go to Database > Tables and verify persons, person_data tables
```

#### Step 1.2: Verify Schema

```bash
# Option A: Via Supabase Dashboard
# 1. Go to Database > Tables
# 2. Verify these tables exist:
#    - persons
#    - person_data
#    - personas (modified)
# 3. Click each table and verify columns

# Option B: Via psql (if you have direct access)
psql "your_connection_string" -c "
SELECT tablename FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;"
```

---

### Phase 2: Data Migration

#### Step 2.1: Run Migration Script (Dry-Run First)

```bash
# Test migration without making changes
python db/migrate_to_person_aggregate.py --dry-run

# Expected output:
# [INFO] PERSON AGGREGATE ROOT MIGRATION
# [INFO] Mode: DRY RUN (no changes)
# [INFO] Found N personas to migrate
# [DRY RUN] Would migrate persona (id=...)
# ...
# [INFO] MIGRATION SUMMARY
# [INFO] Migrated: N
# [INFO] Failed:   0
# [INFO] Skipped:  0
```

#### Step 2.2: Run Migration Script (Live)

```bash
# Perform actual migration
python db/migrate_to_person_aggregate.py

# Expected output:
# [INFO] PERSON AGGREGATE ROOT MIGRATION
# [INFO] Mode: LIVE (changes applied)
# [INFO] Found N personas to migrate
# [INFO] [1/N] Migrating persona ...
# [OK] Migrated successfully (person_id=...)
# ...
# [INFO] MIGRATION SUMMARY
# [INFO] Migrated: N
# [INFO] Failed:   0
# [INFO] Status:   SUCCESS

# Data should now be in new schema
```

#### Step 2.3: Validate Migration Results

```bash
# Check migration results
python db/migrate_to_person_aggregate.py --validate-only

# Expected output:
# [INFO] VALIDATING MIGRATION
# [INFO] Table record counts:
# [INFO]   persons:     N
# [INFO]   person_data: N
# [INFO]   personas:    N
# [INFO] Validating relationships...
# [OK] Relationship validation: [OK]
```

---

### Phase 3: Code Deployment

#### Step 3.1: Deploy Updated Code

```bash
# Merge to main branch (if not already)
git merge epic/09-person-aggregate-root

# Push to GitHub
git push origin main

# Trigger deployment (depends on your CI/CD setup):

# Option A: Cloud Run (Google Cloud)
gcloud run deploy persona-api \
  --source . \
  --region us-central1 \
  --allow-unauthenticated

# Option B: Docker (local or other platforms)
docker build -t persona-api:latest .
docker push your-registry/persona-api:latest
docker pull your-registry/persona-api:latest
docker run -d -p 8080:8080 your-registry/persona-api:latest

# Option C: Manual update
# 1. Download updated code
# 2. Stop running server
# 3. Replace code
# 4. Start running server
```

#### Step 3.2: Verify Deployment

```bash
# Check service is running
curl https://your-api-url/health

# Expected response:
# {"status": "healthy", "service": "persona-api", "environment": "production"}

# Check API documentation
curl https://your-api-url/docs
```

---

## Verification Steps

### Post-Deployment Checks

```bash
# 1. Health check
curl https://your-api-url/health

# 2. Test create person endpoint
curl -X POST https://your-api-url/v1/person \
  -H "Content-Type: application/json"

# 3. Test data submission
PERSON_ID="<response_from_step_2>"
curl -X POST "https://your-api-url/v1/person/{$PERSON_ID}/data" \
  -H "Content-Type: application/json" \
  -d '{
    "raw_text": "Test data for verification",
    "source": "deployment-test"
  }'

# 4. Test data retrieval
curl -X GET "https://your-api-url/v1/person/{$PERSON_ID}/data"

# 5. Test data persistence
curl -X GET "https://your-api-url/v1/person/{$PERSON_ID}"
```

### Database Verification

```bash
# Verify data integrity in Supabase:

# 1. Check persons table has records
SELECT COUNT(*) as persons_count FROM public.persons;

# 2. Check person_data table has records
SELECT COUNT(*) as submissions_count FROM public.person_data;

# 3. Check personas table updated
SELECT COUNT(*) as personas_count FROM public.personas;

# 4. Verify relationships
SELECT
  p.id as person_id,
  COUNT(DISTINCT pd.id) as data_submissions,
  pers.id as persona_id,
  pers.version
FROM public.persons p
LEFT JOIN public.person_data pd ON p.id = pd.person_id
LEFT JOIN public.personas pers ON p.id = pers.person_id
GROUP BY p.id, pers.id, pers.version;
```

---

## Rollback Procedure

### Critical: Backup Restoration

If migration fails or issues are detected, follow these steps:

#### Option 1: Database Restore (Recommended)

```bash
# Via Supabase Dashboard:
# 1. Go to Project > Database > Backups
# 2. Find backup created before migration
# 3. Click "Restore"
# 4. Confirm restoration
# 5. Wait for restoration to complete
# 6. Verify data is restored

# Estimated recovery time: 5-30 minutes depending on database size
```

#### Option 2: Manual Rollback (If Restore Not Available)

```bash
# 1. Stop the application
# 2. Truncate new tables (only if confident)
psql "your_connection_string" -c "
DROP TABLE IF EXISTS public.person_data CASCADE;
DROP TABLE IF EXISTS public.persons CASCADE;
ALTER TABLE public.personas DROP COLUMN IF EXISTS person_id;
ALTER TABLE public.personas DROP COLUMN IF EXISTS version;
ALTER TABLE public.personas DROP COLUMN IF EXISTS computed_from_data_ids;
"

# 3. Deploy previous code version
# 4. Verify application is working

# Note: This approach loses any new data created during failed migration
```

#### Option 3: Partial Rollback (Some Data Recoverable)

```bash
# If only some personas failed to migrate:
# 1. Identify failed personas from migration log
# 2. Delete corresponding person entries created during migration
# 3. Keep successfully migrated data
# 4. Re-run migration for failed personas
```

---

## Monitoring & Troubleshooting

### Monitor Application Logs

```bash
# View application logs
gcloud logging read "resource.type=cloud_run_revision
AND resource.labels.service_name=persona-api" \
  --limit 50 \
  --format json

# Filter for errors
gcloud logging read "severity=ERROR
AND resource.labels.service_name=persona-api" \
  --limit 20
```

### Common Issues and Solutions

#### Issue 1: Migration Script Fails with Database Errors

**Symptom:**
```
Failed to create person: 'persona_id' foreign key constraint
```

**Solution:**
1. Verify schema migration (Phase 1) completed successfully
2. Check that persons table exists: `SELECT tablename FROM pg_tables WHERE tablename='persons'`
3. Verify foreign keys: `SELECT constraint_name FROM information_schema.table_constraints WHERE table_name='person_data'`
4. Re-run schema migration if necessary

#### Issue 2: API Returns 404 for New Endpoints

**Symptom:**
```
{"detail": "Not Found"}
```

**Solution:**
1. Verify code deployment completed: `git log --oneline | head -5`
2. Check application is running: `curl /health`
3. Verify routes are registered: Check application logs for "Include API routes"
4. Redeploy if necessary

#### Issue 3: Data Disappears After Migration

**Symptom:**
```
curl /v1/person returns empty list
```

**Solution:**
1. Verify migration completed: Check migration summary shows "SUCCESSFUL"
2. Check database directly: `SELECT COUNT(*) FROM public.persons`
3. If empty, restore from backup
4. Review migration logs for errors

#### Issue 4: Persona Recomputation Fails

**Symptom:**
```
Failed to regenerate persona: LLM chain error
```

**Solution:**
1. Check OpenAI API key is configured: `echo $OPENAI_API_KEY`
2. Verify LLM service is accessible: `curl https://api.openai.com/v1/models`
3. Check application logs: `gcloud logging read "resource.labels.service_name=persona-api"`
4. Verify sufficient OpenAI quota available
5. If issue persists, data can be submitted without regeneration (data-only endpoint)

### Performance Monitoring

```bash
# Monitor API response times
# Via Application Insights or similar:

# Example: Average response time
SELECT
  endpoint,
  COUNT(*) as request_count,
  AVG(duration_ms) as avg_duration,
  MAX(duration_ms) as max_duration
FROM requests
WHERE timestamp > NOW() - INTERVAL 1 HOUR
GROUP BY endpoint;

# Monitor database performance
# Via Supabase:
# 1. Go to Project > Database > Performance
# 2. Check slow queries
# 3. Review indexes are being used
```

---

## Data Lineage & Versioning

### Understanding the New Schema

Each persona now includes versioning and lineage information:

```json
{
  "id": "uuid-1",
  "person_id": "uuid-2",
  "persona": {
    "name": "John Doe",
    "summary": "...",
    ...
  },
  "version": 1,
  "computed_from_data_ids": [
    "data-id-1",
    "data-id-2"
  ],
  "created_at": "2025-11-09T...",
  "updated_at": "2025-11-09T..."
}
```

### Version History

When new data is added to a person, the persona is recomputed:

```
Initial State:
  Person: {id: person-1}
  Data: [{id: data-1, text: "..."}]
  Persona: {version: 1, computed_from_data_ids: [data-1]}

After New Submission:
  Person: {id: person-1}
  Data: [{id: data-1, text: "..."}, {id: data-2, text: "..."}]
  Persona: {version: 2, computed_from_data_ids: [data-1, data-2]}
```

### Querying Persona History

```sql
-- Get all persona versions for a person
SELECT
  p.id,
  p.version,
  p.created_at,
  ARRAY_LENGTH(p.computed_from_data_ids, 1) as data_submissions_used
FROM public.personas p
WHERE p.person_id = 'specific-person-id'
ORDER BY p.version DESC;

-- Get data used to compute a specific persona
SELECT
  pd.id,
  pd.raw_text,
  pd.source,
  pd.created_at
FROM public.person_data pd
WHERE pd.person_id = 'specific-person-id'
ORDER BY pd.created_at;
```

---

## Post-Deployment Checklist

- [ ] Health checks pass
- [ ] All 8 endpoints working
- [ ] Data migration verified
- [ ] Database relationships validated
- [ ] Logs reviewed for errors
- [ ] Performance metrics normal
- [ ] Team notified of completion
- [ ] Update incident management system
- [ ] Schedule post-mortem if any issues occurred

---

## Support & Escalation

### During Deployment

- **Deployment Engineer**: Monitor deployment progress
- **Database Admin**: Monitor database performance
- **SRE Team**: On-call for infrastructure issues
- **Product Owner**: Monitor for customer impact

### Contact Information

- **Deployment Slack Channel**: #persona-api-deploy
- **Incident Channel**: #incidents
- **On-Call Rotation**: See OpsGenie

### Rollback Authority

- **Automatic**: If health checks fail
- **Manual**: With approval from Engineering Lead
- **Escalation**: Director of Engineering for emergency rollbacks

---

## Timeline Estimates

| Phase | Task | Duration | Notes |
|-------|------|----------|-------|
| 1 | Schema migration | 5-10 min | Typically fast |
| 2 | Data migration | 5-30 min | Depends on data volume |
| 2 | Validation | 5 min | Must pass before proceeding |
| 3 | Code deployment | 5-10 min | Depends on CI/CD |
| 3 | Verification | 10 min | Health checks + manual testing |
| **Total** | **Complete deployment** | **30-60 min** | Including verification |

**Maintenance Window Required**: 1 hour minimum

---

## Questions?

Contact the Engineering Team or refer to:
- IMPLEMENTATION-PLAN.md: Architecture and design decisions
- EPIC-09-INDEX.md: User stories and task breakdown
- Code Comments: Detailed implementation notes in source files
