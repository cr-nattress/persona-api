# Database Setup & Management

This directory contains all database-related files for Persona-API, including schema migrations and documentation.

## Quick Start

### 1. Create Supabase Project

1. Go to [Supabase](https://app.supabase.com)
2. Create a new project
3. Copy the project URL and anonymous key
4. Add to your `.env` file:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
```

### 2. Run Migrations

Apply the SQL migrations to your Supabase database:

1. Open Supabase dashboard → SQL Editor
2. Create a new query
3. Copy the contents of `migrations/001_create_personas_table.sql`
4. Execute the query

The migration will:
- Create the `personas` table
- Add UUID and JSONB support
- Create indexes for performance
- Add automatic `updated_at` timestamps

### 3. Verify Connection

Test that the connection works:

```python
from app.db import get_supabase_client

supabase = get_supabase_client()
if supabase.is_connected():
    print("Connected to Supabase!")
else:
    print("Connection failed")
```

## Schema

### Personas Table

```sql
CREATE TABLE public.personas (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  raw_text TEXT NOT NULL,
  persona JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Columns:**
- `id` (UUID): Unique identifier
- `raw_text` (TEXT): Original unstructured text input
- `persona` (JSONB): Structured persona JSON output
- `created_at` (TIMESTAMPTZ): Creation timestamp
- `updated_at` (TIMESTAMPTZ): Last update timestamp (auto-updated)

**Indexes:**
- `idx_personas_created_at`: For sorting/filtering by creation date
- `idx_personas_updated_at`: For sorting/filtering by update date

## Usage

### Using the Repository Pattern

```python
from app.repositories.persona_repo import get_persona_repository
from app.models.persona import PersonaCreate

repo = get_persona_repository()

# Create
persona_data = PersonaCreate(
    raw_text="Some text about a person",
    persona={"name": "John", "traits": ["friendly"]}
)
created = await repo.create(persona_data)

# Read
persona = await repo.read(created.id)

# Update
from app.models.persona import PersonaUpdate
updated = await repo.update(
    created.id,
    PersonaUpdate(persona={"name": "John", "traits": ["friendly", "smart"]})
)

# Delete
await repo.delete(created.id)

# List all
personas, total = await repo.read_all(limit=10, offset=0)

# Count
count = await repo.count()
```

### Direct Supabase Client

```python
from app.db import get_supabase_client

supabase = get_supabase_client()

# Insert
response = supabase.client.table('personas').insert({
    'raw_text': 'Text',
    'persona': {'key': 'value'}
}).execute()

# Select
response = supabase.client.table('personas').select('*').execute()

# Update
response = supabase.client.table('personas').update({
    'persona': {'updated': True}
}).eq('id', 'some-uuid').execute()

# Delete
response = supabase.client.table('personas').delete().eq('id', 'some-uuid').execute()
```

## Migrations

All migrations are stored in the `migrations/` directory and numbered sequentially:

- `001_create_personas_table.sql` - Initial schema with personas table

### Creating New Migrations

1. Create a new file: `migrations/00N_description.sql`
2. Write your SQL with clear comments
3. Test in Supabase dashboard first
4. Document in this README

## Error Handling

The repository and client include comprehensive error handling:

```python
from postgrest.exceptions import APIError

try:
    persona = await repo.create(data)
except APIError as e:
    print(f"Database error: {e}")
except ValueError as e:
    print(f"Validation error: {e}")
```

## Performance

- Queries are indexed for fast lookups
- Connection uses Supabase's built-in connection pooling
- JSONB allows flexible persona schema without migrations
- Pagination support with `limit` and `offset`

## Backup & Recovery

### Backup

Supabase automatically backs up your data. To manually export:

1. Supabase Dashboard → Database → Backups
2. Or use `pg_dump` with the connection string

### Recovery

1. Supabase Dashboard → Database → Backups
2. Select a backup and restore

## Testing

For testing, use the mock/test utilities:

```python
from app.db import reset_supabase_client

# Reset client between tests
@pytest.fixture(autouse=True)
def reset_db():
    reset_supabase_client()
    yield
    reset_supabase_client()
```

## Troubleshooting

### Connection Issues

**Problem:** "Connection refused"
**Solution:** Check SUPABASE_URL and SUPABASE_ANON_KEY in `.env`

**Problem:** "Authentication failed"
**Solution:** Verify the anonymous key has table access in Supabase RLS policies

### Migration Issues

**Problem:** "Table already exists"
**Solution:** Migrations use `CREATE TABLE IF NOT EXISTS`, this is safe to rerun

**Problem:** "Permission denied"
**Solution:** Check your Supabase user role and RLS policies

## Security

- Never commit `.env` with real credentials
- Use `.env.example` as a template
- Supabase provides automatic RLS (Row Level Security) setup
- Consider enabling additional RLS policies for production

## Next Steps

1. [EPIC-03: Core LLM Chain](../backlog/epic-03-core-llm-chain/EPIC.md) - Implement persona generation
2. [EPIC-04: API Endpoints](../backlog/epic-04-api-endpoints/EPIC.md) - Expose database operations via REST

---

For detailed task instructions, see `backlog/epic-02-database-design/`
