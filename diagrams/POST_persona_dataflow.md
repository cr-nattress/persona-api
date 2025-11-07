# POST /v1/persona Data Flow Diagram

Complete request-to-response data flow for creating personas via the REST API.

---

## High-Level Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         HTTP POST Request                                   │
│                        /v1/persona Endpoint                                 │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  1. API Route Handler (create_persona)                                       │
│     • Accept PersonaCreate model                                             │
│     • Validate request with Pydantic                                         │
│     • Extract raw_text and optional persona                                  │
└──────────────────────────────┬───────────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  2. PersonaService Layer (generate_persona)                                  │
│     • Orchestrate business logic                                             │
│     • Delegate to synthesizer                                                │
│     • Handle service-level errors                                            │
└──────────────────────────────┬───────────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  3. PersonaSynthesizer (generate_and_save_persona)                           │
│     • Coordinate LLM generation with persistence                             │
│     • Manage workflow orchestration                                          │
└──────────────────────────────┬───────────────────────────────────────────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
     ┌──────────────────────┐    ┌──────────────────────┐
     │  4a. LLM Chain       │    │  4b. OpenAI API      │
     │  (2-Step Pipeline)   │◄──►│  (gpt-4o-mini)       │
     └──────────────────────┘    └──────────────────────┘
            │
            │ (Step 1: Clean)
            ├─────────────────────────────────────────┐
            │                                         │
            ▼                                         │
     ┌─────────────────────────┐            ┌────────┴──────────┐
     │  Step 1: Clean Text     │            │  OpenAI Request   │
     │  • Normalize raw text   │            │  • System prompt  │
     │  • Extract key facts    │            │  • User input     │
     │  • Structure as notes   │            │  • Temperature: 0.7
     └─────────────────────────┘            │  • Max tokens: 2000
            │                               └───────────────────┘
            │ (cleaned_text)
            │
            ├─────────────────────────────────────────┐
            │                                         │
            ▼                                         │
     ┌─────────────────────────┐            ┌────────┴──────────┐
     │  Step 2: Populate       │            │  OpenAI Request   │
     │  • Generate persona JSON│            │  • System prompt  │
     │  • Populate all fields  │            │  • User input     │
     │  • Parse JSON response  │            │  • Temperature: 0.7
     └─────────────────────────┘            │  • Max tokens: 2000
            │                               └───────────────────┘
            │ (persona_json)
            │
            └──────────────────────────────┐
                                           │
                                           ▼
                                ┌──────────────────────────┐
                                │  Create PersonaCreate    │
                                │  Model Instance          │
                                │  • raw_text (input)      │
                                │  • persona (LLM output)  │
                                │  • Add metadata          │
                                └──────────────┬───────────┘
                                              │
                                              ▼
                                ┌──────────────────────────┐
                                │  5. Repository Layer     │
                                │  (create operation)      │
                                │  • Build INSERT data     │
                                │  • Supabase client call  │
                                │  • Parse response        │
                                └──────────────┬───────────┘
                                              │
                                              ▼
                                ┌──────────────────────────┐
                                │  6. Supabase Database    │
                                │  (PostgreSQL)            │
                                │  • Execute INSERT        │
                                │  • Generate UUID (id)    │
                                │  • Set timestamps        │
                                │  • Return full record    │
                                └──────────────┬───────────┘
                                              │
                                              ▼
                                ┌──────────────────────────┐
                                │  7. PersonaInDB Model    │
                                │  • id (UUID)             │
                                │  • raw_text              │
                                │  • persona (JSON)        │
                                │  • created_at            │
                                │  • updated_at            │
                                └──────────────┬───────────┘
                                              │
                                              ▼
                                ┌──────────────────────────┐
                                │  8. Response Assembly    │
                                │  • Convert to Response   │
                                │  • Set HTTP 201 status   │
                                │  • Serialize to JSON     │
                                └──────────────┬───────────┘
                                              │
                                              ▼
                                ┌──────────────────────────┐
                                │  HTTP 201 Response       │
                                │  {                       │
                                │    "id": "UUID",         │
                                │    "raw_text": "...",    │
                                │    "persona": {...},     │
                                │    "created_at": "...",  │
                                │    "updated_at": "..."   │
                                │  }                       │
                                └──────────────────────────┘
```

---

## Detailed Component Breakdown

### 1. API Route Handler: `create_persona` (app/api/routes.py:39-89)

**Entry Point**: `POST /v1/persona`

**Request Model**: `PersonaCreate`
```json
{
  "raw_text": "unstructured text about person",
  "persona": null  // optional, can be pre-populated
}
```

**Processing Steps**:
1. FastAPI receives HTTP POST request
2. Pydantic validates against `PersonaCreate` schema
3. Extract `raw_text` from validated request
4. Log request details (text length)
5. Get PersonaService singleton instance
6. Call `service.generate_persona(raw_text)`

**Error Handling**:
- `ValueError` → HTTP 400 Bad Request
- Any other exception → HTTP 500 Internal Server Error

**Response Model**: `PersonaResponse`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "raw_text": "...",
  "persona": { /* full structured persona */ },
  "created_at": "2024-11-07T10:30:00.000000",
  "updated_at": "2024-11-07T10:30:00.000000"
}
```

**HTTP Status**: `201 Created`

---

### 2. Service Layer: `PersonaService.generate_persona` (app/services/persona_service.py:32-46)

**Purpose**: High-level business logic orchestration

**Input**: Raw text string (optional: pre-populated persona)

**Processing**:
1. Log persona generation start
2. Get PersonaSynthesizer singleton
3. Call `synthesizer.generate_and_save_persona(raw_text)`
4. Return PersonaInDB result

**Data Flow**:
```
raw_text (string)
    │
    ▼
PersonaSynthesizer.generate_and_save_persona()
    │
    ▼
PersonaInDB (with id, timestamps)
```

---

### 3. Synthesizer: `PersonaSynthesizer.generate_and_save_persona` (app/services/persona_synthesizer.py:25-71)

**Purpose**: Coordinate LLM generation with database persistence

**Workflow**:

#### Step 3a: LLM Chain Generation
```
Input: raw_text (string)
    │
    ▼
PersonaLLMChain.generate_persona()
    │
    ├─ Step 1: Clean text (via OpenAI)
    │   • Input: raw_text
    │   • Process: Text normalization, fact extraction
    │   • Output: cleaned_text (structured notes)
    │
    └─ Step 2: Populate persona (via OpenAI)
        • Input: cleaned_text
        • Process: Generate comprehensive persona JSON
        • Output: persona_json (Dict[str, Any])

Output: persona_json (dictionary)
```

#### Step 3b: Model Creation
```
PersonaCreate(
    raw_text=raw_text,
    persona=persona_json
)
```

#### Step 3c: Database Persistence
```
PersonaRepository.create(persona_create)
    │
    ▼
PersonaInDB (from database with id, timestamps)
```

---

### 4. LLM Chain: Two-Step Persona Generation Pipeline

#### 4a. Step 1: Text Cleaning (step1_clean_text)

**Model**: OpenAI `gpt-4o-mini`

**Configuration**:
- Temperature: 0.7
- Max Tokens: 2000
- API Key: From environment

**Prompts**:
- **System Prompt** (step1_clean_system.txt): Instructions for cleaning strategy
- **User Prompt** (step1_clean_user.txt): Template for raw_text input

**Processing**:
```
Input: raw_text
    │
    ▼
OpenAI ChatCompletion API Call
    │
    ├─ Message 1: System role with instructions
    ├─ Message 2: User role with raw_text
    │
    ▼
LLM Response: cleaned_text (string)
    │
    ├─ Normalize formatting
    ├─ Extract key facts
    ├─ Structure as bullet points
    └─ Remove noise/irrelevant content

Output: cleaned_text (structured notes string)
```

**Example Output Format**:
```
- Name: John Smith
- Role: Software Engineer
- Experience: 10 years
- Skills: Python, AWS, System Design
- Location: San Francisco, CA
- Education: BS Computer Science
- ...
```

---

#### 4b. Step 2: Persona Population (step2_populate_persona)

**Model**: OpenAI `gpt-4o-mini`

**Configuration**:
- Temperature: 0.7
- Max Tokens: 2000

**Prompts**:
- **System Prompt** (step2_persona_system.txt): JSON schema instructions
- **User Prompt** (step2_persona_user.txt): Template for cleaned_text input

**Processing**:
```
Input: cleaned_text
    │
    ▼
OpenAI ChatCompletion API Call
    │
    ├─ Message 1: System role with schema
    ├─ Message 2: User role with cleaned_text
    │
    ▼
LLM Response: persona_text (string, may contain JSON)
    │
    ├─ Extract JSON from response
    │  (handles markdown code blocks)
    ├─ Parse JSON safely
    └─ Validate structure

Output: persona_json (Dict[str, Any])
```

**Expected JSON Structure**:
```json
{
  "meta": {
    "name": "John Smith",
    "role": "Software Engineer",
    "location": "San Francisco, CA"
  },
  "identity": {
    "core_description": "..."
  },
  "professional": {
    "title": "Senior Engineer",
    "experience": [...]
  },
  "skills": [...],
  "education": [...],
  "_meta": {
    "raw_text_length": 5000,
    "cleaned_text_length": 1500,
    "model_used": "gpt-4o-mini"
  }
}
```

---

### 5. Repository Layer: Data Persistence (app/repositories/persona_repo.py:30-69)

**Purpose**: Abstract database operations

**Method**: `create(persona: PersonaCreate) -> PersonaInDB`

**Processing**:

```
Input: PersonaCreate model
    {
        "raw_text": "...",
        "persona": { ... }
    }
    │
    ▼
Build Supabase INSERT data
    {
        "raw_text": "...",
        "persona": { ... }
    }
    │
    ▼
Supabase Client Call
    supabase.client.table("personas")
        .insert(data)
        .execute()
    │
    ▼
Database Response
    [
        {
            "id": "550e8400-...",
            "raw_text": "...",
            "persona": { ... },
            "created_at": "2024-11-07T10:30:00.000000",
            "updated_at": "2024-11-07T10:30:00.000000"
        }
    ]
    │
    ▼
Parse Response
    PersonaInDB(**result)
    │
    ▼
Return PersonaInDB
```

**Database Operations**:

| Operation | SQL | Handler |
|-----------|-----|---------|
| INSERT | `INSERT INTO personas (raw_text, persona) VALUES (?, ?)` | `repository.create()` |
| UUID Gen | Database auto-generates UUID | PostgreSQL DEFAULT |
| Timestamp | Database auto-sets `created_at`, `updated_at` | PostgreSQL DEFAULT |

---

### 6. Database: Supabase PostgreSQL

**Table Schema**: `personas`

```sql
CREATE TABLE personas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    raw_text TEXT NOT NULL,
    persona JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

**Data Storage**:
- **id**: Unique identifier (auto-generated UUID)
- **raw_text**: Original unstructured input (TEXT)
- **persona**: Generated persona structure (JSONB for indexing)
- **created_at**: Insertion timestamp (auto-set)
- **updated_at**: Last modification timestamp (auto-set)

---

### 7. Response Assembly

**Step 1**: Convert PersonaInDB to PersonaResponse
```python
PersonaResponse(**persona_in_db.model_dump())
```

**Step 2**: Set HTTP Status Code
```
HTTP 201 Created
```

**Step 3**: Serialize to JSON
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "raw_text": "Unstructured profile text...",
  "persona": {
    "meta": { "name": "...", "role": "..." },
    "identity": { "core_description": "..." },
    "professional": { ... },
    "skills": [ ... ],
    "education": [ ... ],
    "_meta": { "model_used": "gpt-4o-mini" }
  },
  "created_at": "2024-11-07T10:30:00.000000",
  "updated_at": "2024-11-07T10:30:00.000000"
}
```

---

## Error Handling Paths

### Path 1: Request Validation Error

```
POST /v1/persona
{
  "invalid_field": "value"
}
    │
    ▼
Pydantic Validation Fails
    │
    ▼
FastAPI Exception Handler
    │
    ▼
HTTP 422 Unprocessable Entity
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "raw_text"],
      "msg": "Field required"
    }
  ]
}
```

### Path 2: LLM Generation Error

```
LLM Chain Execution
    │
    ▼
OpenAI API Error (rate limit, invalid key, etc.)
    │
    ▼
ValueError Exception
    │
    ▼
Service Error Handler
    │
    ▼
HTTPException (400 Bad Request)
{
  "detail": "Text cleaning failed: OpenAI API error"
}
```

### Path 3: Database Error

```
Repository.create()
    │
    ▼
Supabase API Error (connection, constraint, etc.)
    │
    ▼
APIError Exception
    │
    ▼
Repository Error Handler
    │
    ▼
Exception re-raised to Service
    │
    ▼
HTTPException (500 Internal Server Error)
{
  "detail": "Failed to generate persona. Please try again."
}
```

### Path 4: JSON Parsing Error

```
LLM Response Text
    │
    ▼
_safe_json_parse()
    │
    ├─ Try direct JSON parse
    ├─ Try markdown code block extraction
    ├─ Try object bracket extraction
    │
    ▼
If all fail: ValueError
    │
    ▼
HTTPException (400 Bad Request)
{
  "detail": "Persona generation failed: Could not parse JSON response"
}
```

---

## Data Transformations

### Transformation 1: Raw Text → Cleaned Text

```
Input (raw_text):
"John Doe
Software Engineer at TechCorp
10 years experience
Python, AWS, Kubernetes
San Francisco, CA"

    │
    ▼ [LLM Step 1: Clean]
    │
Output (cleaned_text):
"- Name: John Doe
- Title: Software Engineer
- Company: TechCorp
- Experience: 10 years
- Primary Skills: Python, AWS, Kubernetes
- Location: San Francisco, California
- Expertise Level: Senior"
```

### Transformation 2: Cleaned Text → Persona JSON

```
Input (cleaned_text):
"- Name: John Doe
- Title: Software Engineer
[...]"

    │
    ▼ [LLM Step 2: Populate]
    │
Output (persona_json):
{
  "meta": {
    "name": "John Doe",
    "role": "Software Engineer",
    "location": "San Francisco, CA"
  },
  "identity": {
    "core_description": "Experienced software engineer..."
  },
  "professional": {
    "title": "Senior Software Engineer",
    "company": "TechCorp",
    "years_experience": 10,
    "experience_history": [...]
  },
  "skills": [
    {"name": "Python", "proficiency": "expert"},
    {"name": "AWS", "proficiency": "expert"},
    {"name": "Kubernetes", "proficiency": "advanced"}
  ]
}
```

### Transformation 3: Persona JSON → Database Record

```
Input (PersonaCreate):
{
  "raw_text": "John Doe...",
  "persona": { ... }
}

    │
    ▼ [INSERT into PostgreSQL]
    │
Output (PersonaInDB):
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "raw_text": "John Doe...",
  "persona": { ... },
  "created_at": "2024-11-07T10:30:00.000000",
  "updated_at": "2024-11-07T10:30:00.000000"
}
```

---

## Data Flow Sequence Diagram (Text-based)

```
Client                 API Route              Service            Synthesizer         LLM Chain           Repository         Database
│                         │                      │                   │                    │                    │                   │
├─ POST /v1/persona ──────►│                      │                   │                    │                    │                   │
│                         │                      │                    │                    │                    │                   │
│                         ├─ Validate ──────────►│                    │                    │                    │                   │
│                         │   (PersonaCreate)    │                    │                    │                    │                   │
│                         │                      │                    │                    │                    │                   │
│                         │                      ├─ generate_persona─►│                    │                    │                   │
│                         │                      │                    │                    │                    │                   │
│                         │                      │                    ├─ LLM Chain ──────►│                    │                   │
│                         │                      │                    │                    │                    │                   │
│                         │                      │                    │     ┌─ Step 1: Clean text via OpenAI API ──┐     │
│                         │                      │                    │     │                                        │     │
│                         │                      │                    │◄────┤ OpenAI Returns: cleaned_text          │     │
│                         │                      │                    │     └────────────────────────────────────────┘     │
│                         │                      │                    │                    │                    │                   │
│                         │                      │                    │     ┌─ Step 2: Populate persona via OpenAI API ┐  │
│                         │                      │                    │     │                                        │  │
│                         │                      │                    │◄────┤ OpenAI Returns: persona_json (Dict)    │  │
│                         │                      │                    │     └────────────────────────────────────────┘  │
│                         │                      │                    │                    │                    │                   │
│                         │                      │◄─ persona_json ────│                    │                    │                   │
│                         │                      │  (Dict[str, Any])  │                    │                    │                   │
│                         │                      │                    │                    │                    │                   │
│                         │                      │                    ├─ Create PersonaCreate────────────────────────► │
│                         │                      │                    │                    │                    │                   │
│                         │                      │                    │                    │        repository.create()────┐      │
│                         │                      │                    │                    │        (INSERT operation)    │      │
│                         │                      │                    │                    │                    │        ├─ Generate UUID
│                         │                      │                    │                    │                    │        │
│                         │                      │                    │                    │                    │        ├─ Set Timestamps
│                         │                      │                    │                    │                    │        │
│                         │                      │                    │                    │                    │        ├─ Execute INSERT
│                         │                      │                    │                    │                    │        │
│                         │                      │                    │                    │                    │◄───────┤
│                         │                      │                    │                    │                    │        │
│                         │                      │                    │                    │                    │        └──► PersonaInDB
│                         │                      │◄─ PersonaInDB ─────┤◄─ PersonaInDB ─────┤◄─ PersonaInDB ────┤
│                         │                      │  (with id)        (with id)          (with id)
│                         │                      │                    │                    │                    │
│◄─ HTTP 201 Created ────┤◄─ PersonaResponse ──┤                    │                    │                    │
│  (JSON Body)          │   (JSON)             │                    │                    │                    │
│                         │                      │                    │                    │                    │                   │
```

---

## Code Reference Map

| Layer | File | Key Functions |
|-------|------|----------------|
| **API Route** | `app/api/routes.py` | `create_persona()` (lines 39-89) |
| **Service** | `app/services/persona_service.py` | `PersonaService.generate_persona()` (lines 32-46) |
| **Synthesizer** | `app/services/persona_synthesizer.py` | `PersonaSynthesizer.generate_and_save_persona()` (lines 25-71) |
| **LLM Chain** | `app/services/llm_chain.py` | `PersonaLLMChain.generate_persona()` (lines 196-231) |
| **Repository** | `app/repositories/persona_repo.py` | `PersonaRepository.create()` (lines 30-69) |
| **Models** | `app/models/persona.py` | `PersonaCreate`, `PersonaInDB`, `PersonaResponse` |
| **Database** | Supabase PostgreSQL | `personas` table |

---

## Performance Characteristics

### Time Complexity
- **LLM Processing (Step 1 + Step 2)**: ~5-15 seconds (OpenAI API latency)
- **Database INSERT**: ~100-500ms (Supabase latency)
- **Request Validation**: <10ms (Pydantic)
- **Total End-to-End**: ~5-16 seconds

### Space Complexity
- **In-Memory Raw Text**: O(n) where n = text length
- **In-Memory Persona JSON**: O(m) where m = structured output size
- **Database Storage**: O(n + m) for persistence

### Bottlenecks
1. **OpenAI API Latency** (primary): ~5-15 seconds per request
2. **Network I/O**: ~1-3 seconds for database calls
3. **JSON Parsing**: <100ms for typical payloads

---

## Dependencies & External Services

| Component | Service | Key Config |
|-----------|---------|-----------|
| **LLM** | OpenAI API | `gpt-4o-mini` model, temp=0.7, max_tokens=2000 |
| **Database** | Supabase PostgreSQL | Connection via environment variables |
| **Validation** | Pydantic | `BaseModel` schemas |
| **HTTP Server** | FastAPI/Uvicorn | Port 8080 (default) |
| **Logging** | Python logging | Configured via `app.core.logging` |

---

## Validation & Schema Enforcement

### Input Validation (Request)
```python
# PersonaCreate (from Pydantic)
class PersonaCreate(BaseModel):
    raw_text: str  # Required, non-empty
    persona: Optional[Dict[str, Any]] = None  # Optional pre-populated
```

### Output Validation (Response)
```python
# PersonaResponse (from Pydantic)
class PersonaResponse(BaseModel):
    id: UUID  # Required, auto-generated
    raw_text: str  # Required
    persona: Optional[Dict[str, Any]]  # Optional
    created_at: datetime  # Required, auto-set
    updated_at: datetime  # Required, auto-set
```

### Database Validation
- **id**: UUID PRIMARY KEY (auto-generated)
- **raw_text**: TEXT NOT NULL
- **persona**: JSONB (nullable, indexed)
- **created_at/updated_at**: TIMESTAMP WITH TIME ZONE (auto-managed)

---

## Example Request/Response Cycle

### Request
```bash
curl -X POST http://localhost:8080/v1/persona \
  -H "Content-Type: application/json" \
  -d '{
    "raw_text": "John is a senior software engineer with 10 years of experience in Python and AWS. He works at TechCorp in San Francisco and has a degree in Computer Science from MIT."
  }'
```

### Processing Timeline
1. **0ms**: HTTP POST arrives at FastAPI
2. **5ms**: Pydantic validation completes
3. **10ms**: API route handler invokes service
4. **15ms**: Service invokes synthesizer
5. **20ms**: Synthesizer calls LLM chain
6. **5-8 seconds**: LLM Step 1 (text cleaning) - OpenAI API
7. **5-8 seconds**: LLM Step 2 (persona population) - OpenAI API
8. **200ms**: Repository creates database record
9. **300ms**: Response assembly & serialization
10. **~10.5 seconds total**: HTTP 201 response sent to client

### Response
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "raw_text": "John is a senior software engineer...",
  "persona": {
    "meta": {
      "name": "John",
      "role": "Senior Software Engineer",
      "location": "San Francisco, CA"
    },
    "professional": {
      "title": "Senior Software Engineer",
      "company": "TechCorp",
      "years_experience": 10
    },
    "skills": [
      {"name": "Python", "proficiency": "expert"},
      {"name": "AWS", "proficiency": "expert"}
    ],
    "education": [
      {"degree": "Bachelor of Science", "field": "Computer Science", "institution": "MIT"}
    ],
    "_meta": {
      "raw_text_length": 173,
      "cleaned_text_length": 487,
      "model_used": "gpt-4o-mini"
    }
  },
  "created_at": "2024-11-07T10:30:45.123456",
  "updated_at": "2024-11-07T10:30:45.123456"
}
```

---

## Testing Checklist

- [ ] Request validation: Missing `raw_text` → 422
- [ ] Request validation: Invalid JSON → 422
- [ ] LLM API error handling: Rate limit → 400
- [ ] Database connection error → 500
- [ ] JSON parsing failure → 400
- [ ] Successful persona generation → 201
- [ ] Persona ID uniqueness: Each creation gets new UUID
- [ ] Timestamp auto-generation: `created_at` equals `updated_at` on creation
- [ ] Response structure: All required fields present
- [ ] Persona JSON structure: Expected schema validation

---

## Deployment Considerations

1. **Environment Variables Required**:
   - `OPENAI_API_KEY`: For LLM access
   - `SUPABASE_URL`: Database connection
   - `SUPABASE_KEY`: Database authentication

2. **Rate Limiting**:
   - OpenAI: Check API rate limits
   - Supabase: Monitor database connection pool
   - FastAPI: Implement request throttling if needed

3. **Logging**:
   - Debug logs: Input text samples, LLM response chunks
   - Info logs: Request start/completion, ID generation
   - Error logs: Full stack traces with context

4. **Monitoring**:
   - Track average generation time (should be 5-15s)
   - Monitor OpenAI API costs
   - Alert on database connection failures
