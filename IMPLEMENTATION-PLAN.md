# 🧠 Persona-API

Persona-API is a lightweight Python service that transforms unstructured text into a structured **persona definition JSON**.  
It uses **LangChain + OpenAI** to clean, optimize, and fill out a structured profile describing identity, cognition, behavior, and preferences — ready for use in AI agents, LangGraph flows, or simulations.

---

## 🚀 Objective

> **Persona-API** transforms raw human data (text) into structured persona definitions that describe how someone thinks, decides, and communicates.

It does this by:
1. Cleaning and optimizing messy text input.
2. Generating a JSON persona file using a consistent template.
3. Persisting results to **Supabase** and returning the generated ID + persona.

---

## 🧩 Architecture Overview

| Layer | Description |
|-------|--------------|
| **FastAPI** | Exposes simple REST endpoints (`POST`, `GET`, `PATCH`). |
| **LangChain + OpenAI** | Two-step LLM pipeline (clean → populate persona JSON). |
| **Supabase** | Stores `id`, `raw_text`, and generated `persona` JSON. |
| **Logging (Loguru)** | Logs every potentially error-prone step. |
| **Prompts Folder** | All system and user prompt templates live outside the code. |

---

## 🧱 System Design

### ⚙️ Endpoints

| Method | Route | Description |
|---------|--------|--------------|
| `POST /v1/persona` | Create a persona from raw text input. Returns `{ id, persona }`. |
| `GET /v1/persona/{id}` | Retrieve a previously created persona. |
| `PATCH /v1/persona/{id}` | Re-create and merge persona using new text data. |

### 🧠 Flow
1. **Receive text input**
2. **Step 1 (LLM):** Clean + normalize → concise bullet-point summary
3. **Step 2 (LLM):** Fill out `persona_json_template.json`
4. **Store + return** the resulting persona and unique ID

---

## 🧰 Tech Stack

| Component | Technology |
|------------|-------------|
| API | FastAPI |
| Language Model | LangChain + OpenAI GPT-4o-mini |
| Database | Supabase (Postgres) |
| Logging | Loguru |
| Configuration | dotenv |
| Schema Validation | Pydantic v2 |
| Environment | Python 3.10+ |

---

## 🗂️ Project Structure

persona_api/
├─ app/
│ ├─ main.py
│ ├─ api/routes.py
│ ├─ core/{config.py, logging.py}
│ ├─ db/supabase_client.py
│ ├─ models/persona.py
│ ├─ repositories/persona_repo.py
│ └─ services/
│ ├─ persona_service.py
│ ├─ persona_synthesizer.py
│ └─ llm_chain.py
├─ prompts/
│ ├─ step1_clean_system.txt
│ ├─ step1_clean_user.txt
│ ├─ step2_persona_system.txt
│ ├─ step2_persona_user.txt
│ └─ persona_json_template.json
├─ requirements.txt
└─ README.md

pgsql
Copy code

---

## 🧮 Database Schema (Supabase)

```sql
create extension if not exists "uuid-ossp";

create table if not exists public.personas (
  id uuid primary key default uuid_generate_v4(),
  raw_text text not null,
  persona jsonb not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
🔧 Setup
1. Environment
Create a .env file:

bash
Copy code
SUPABASE_URL=https://YOURPROJECT.supabase.co
SUPABASE_ANON_KEY=YOUR_SUPABASE_KEY
OPENAI_API_KEY=sk-...
2. Install dependencies
bash
Copy code
pip install -r requirements.txt
3. Run server
bash
Copy code
uvicorn app.main:app --reload --port 8080
🧠 How It Works (LangChain Flow)
Step 1 — Clean / Normalize
Prompt: prompts/step1_clean_system.txt + step1_clean_user.txt

Model output: concise bullet summary (values, motivations, tone, etc.)

Step 2 — Populate Persona JSON
Prompt: prompts/step2_persona_system.txt + step2_persona_user.txt

Model receives the cleaned notes + template JSON and fills out as much as possible.

Example internal pseudo-chain
scss
Copy code
raw_text
  ↓
[ChatOpenAI] step1_clean_normalize()
  ↓
clean_notes
  ↓
[ChatOpenAI] step2_populate_persona()
  ↓
persona JSON (validated & stored)
🧾 Example Requests
Create
bash
Copy code
curl -X POST http://localhost:8080/v1/persona \
  -H "Content-Type: application/json" \
  -d '{"text":"Values: Integrity, Curiosity; Motivations: build useful systems; Roles: Engineer, Manager; Interests: AI, Architecture; Tools: C#, Node; Tone: encouraging, direct."}'
Response

json
Copy code
{
  "id": "1c8c4d5b-9f33-4c78-9d2d-bb47f7c2d0e1",
  "persona": {
    "meta": { "...": "..." },
    "identity": { "...": "..." },
    "...": "..."
  }
}
Get
bash
Copy code
curl http://localhost:8080/v1/persona/1c8c4d5b-9f33-4c78-9d2d-bb47f7c2d0e1
Update
bash
Copy code
curl -X PATCH http://localhost:8080/v1/persona/1c8c4d5b-9f33-4c78-9d2d-bb47f7c2d0e1 \
  -H "Content-Type: application/json" \
  -d '{"text":"Interests: LangGraph, Agno; Tools: Python; Style: concise, lightly humorous."}'
🧩 Design Patterns Used
Pattern	Purpose
Repository Pattern	Separates DB logic (persona_repo) from business logic.
Service Layer	Coordinates LangChain calls + repo operations.
Config + Logging	Centralized environment & logging setup.
Prompt Externalization	All LLM instructions live outside code for easy tuning.
Two-Step LLM Chain	Clean → Populate ensures reliability and clarity.

🛠️ Future Enhancements
Area	Idea
LangGraph	Replace llm_chain.py with a proper LangGraph node graph.
Validation	Add JSON Schema validation before saving.
Caching	Use Supabase or local cache to avoid re-processing identical inputs.
Async Jobs	Offload long LLM calls using Celery or BackgroundTasks.
UI	Add a small front-end playground for persona generation.

🧑‍💻 Debugging
All LLM calls, Supabase operations, and JSON parsing steps are logged via Loguru.

Logs show file, function, and line numbers automatically.

If a JSON parsing error occurs, _safe_json_loads() tries to recover partial output.

Use --reload mode while developing; logs print to console.

✅ Summary
Persona-API is designed to be:

Simple to read: clear file structure, minimal magic.

Safe to extend: just swap models or prompts.

Easy to debug: built-in structured logging.

Future-ready: can evolve into a LangGraph or Agno-based agent builder.

“Turns raw context into a digital mind.”

yaml
Copy code
