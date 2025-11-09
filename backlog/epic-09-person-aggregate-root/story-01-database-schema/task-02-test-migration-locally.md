# TASK-09-01-02: Test Migration Locally

**Story**: US-09-01: Create Database Schema

**Estimated Time**: 45 minutes

**Description**: Apply the migration SQL to your local development database and verify that all tables, constraints, and indexes are created correctly. Test rollback capability.

## Agent Prompt

You are implementing EPIC-09: Person Aggregate Root with Unstructured Data History.

**Goal**: Apply the migration SQL to a local database and verify it works correctly, including testing rollback.

**Context**: We need to ensure the migration is production-ready before committing. This involves applying it to a local Supabase instance or PostgreSQL database and verifying all tables exist with correct structure.

**Instructions**:

1. **Connect to your local database**:
   - Use your local Supabase instance or PostgreSQL
   - Ensure you're not pointing to production
   - Have a backup or use a test database

2. **Apply the migration**:
   - Execute the SQL migration file you created
   - Check for any errors (constraint violations, syntax errors, etc.)
   - Verify no other tables or data were affected

3. **Verify table creation**:
   ```sql
   -- Check tables exist
   SELECT table_name FROM information_schema.tables
   WHERE table_schema = 'public'
   AND table_name IN ('persons', 'person_data', 'personas');

   -- Should return 3 rows:
   -- persons
   -- person_data
   -- personas
   ```

4. **Verify table structure**:
   ```sql
   -- Check persons table
   \d public.persons

   -- Check person_data table
   \d public.person_data

   -- Check personas table
   \d public.personas
   ```

5. **Verify constraints**:
   ```sql
   -- List all constraints
   SELECT constraint_name, table_name, constraint_type
   FROM information_schema.table_constraints
   WHERE table_schema = 'public'
   AND table_name IN ('persons', 'person_data', 'personas');

   -- Should include:
   -- pk_persons_id
   -- fk_person_data_person
   -- fk_personas_person
   ```

6. **Verify indexes**:
   ```sql
   -- List all indexes
   SELECT indexname FROM pg_indexes
   WHERE schemaname = 'public'
   AND tablename IN ('persons', 'person_data', 'personas');

   -- Should include:
   -- idx_person_data_person_id
   -- idx_person_data_created_at
   -- idx_personas_person_id
   -- idx_personas_updated_at
   ```

7. **Test basic operations**:
   ```sql
   -- Insert test person
   INSERT INTO public.persons (id) VALUES (uuid_generate_v4())
   RETURNING id;
   -- Should succeed

   -- Try to insert person_data
   INSERT INTO public.person_data (person_id, raw_text, source)
   VALUES ((SELECT id FROM public.persons LIMIT 1), 'test data', 'api')
   RETURNING id;
   -- Should succeed

   -- Try to insert persona
   INSERT INTO public.personas (person_id, persona, computed_from_data_ids, version)
   VALUES (
     (SELECT id FROM public.persons LIMIT 1),
     '{"test": "persona"}'::jsonb,
     ARRAY[uuid_generate_v4()],
     1
   )
   RETURNING id;
   -- Should succeed
   ```

8. **Test CASCADE DELETE**:
   ```sql
   -- Delete person
   DELETE FROM public.persons WHERE id = (SELECT person_id FROM public.personas LIMIT 1);

   -- Verify related data deleted
   SELECT COUNT(*) FROM public.person_data WHERE person_id IS NULL;
   -- Should be 0

   SELECT COUNT(*) FROM public.personas WHERE person_id IS NULL;
   -- Should be 0
   ```

9. **Rollback test** (optional):
   - Note the migration number
   - Create a rollback script if using version control
   - Test rollback in local database
   - Verify tables still exist after rollback (or are properly removed)

## Verification Steps

1. ✅ All three tables exist in public schema
2. ✅ persons table has correct columns (id, created_at, updated_at)
3. ✅ person_data has correct columns and FK to persons
4. ✅ personas table has version, computed_from_data_ids, person_id UNIQUE
5. ✅ All indexes created successfully
6. ✅ Foreign key constraints work (enforced)
7. ✅ CASCADE DELETE works (test above)
8. ✅ INSERT/UPDATE/DELETE operations work correctly
9. ✅ No data loss from existing tables

## Expected Outcome

- All three tables successfully created in local database
- All constraints enforced
- All indexes created
- Basic CRUD operations work
- CASCADE DELETE behavior verified
- Ready for next step (schema verification)

## Estimated Time: 45 minutes

---

**Success Criteria**: Migration applies cleanly with no errors, all tables and constraints verify correctly, basic operations work.
