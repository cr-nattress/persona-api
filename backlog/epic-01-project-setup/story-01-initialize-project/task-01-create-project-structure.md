# TASK-01-01-01: Create Project Directory Structure

**Story:** US-01-01

**Estimated Time:** 10 minutes

**Description:** Create the complete directory structure for the Persona-API project following Python best practices.

## Agent Prompt

You are implementing **EPIC-01: Project Setup & Infrastructure**.

**Goal:** Create a properly organized Python project directory structure for a FastAPI + LangChain + Supabase application.

**Context:** This is the foundation of the project. A good directory structure makes the codebase easy to navigate, scale, and maintain.

**Instructions:**

1. Create the main application directories at the project root:
   ```
   mkdir -p app/api
   mkdir -p app/core
   mkdir -p app/db
   mkdir -p app/models
   mkdir -p app/repositories
   mkdir -p app/services
   mkdir -p prompts
   mkdir -p tests/test_api
   mkdir -p tests/test_services
   ```

2. Create `__init__.py` files in each Python package directory:
   - `app/__init__.py`
   - `app/api/__init__.py`
   - `app/core/__init__.py`
   - `app/db/__init__.py`
   - `app/models/__init__.py`
   - `app/repositories/__init__.py`
   - `app/services/__init__.py`
   - `tests/__init__.py`
   - `tests/test_api/__init__.py`
   - `tests/test_services/__init__.py`

3. Create placeholder files for main modules (these will be filled later):
   - `app/main.py` (FastAPI app initialization)
   - `app/api/routes.py` (API routes)
   - `app/core/config.py` (configuration)
   - `app/core/logging.py` (logging setup)
   - `app/db/supabase_client.py` (database client)
   - `app/models/persona.py` (data models)
   - `app/repositories/persona_repo.py` (repository)
   - `app/services/persona_service.py` (service layer)
   - `app/services/persona_synthesizer.py` (business logic)
   - `app/services/llm_chain.py` (LLM integration)

4. Each placeholder file should contain a minimal docstring indicating its purpose:
   ```python
   \"\"\"
   Module description.
   \"\"\"
   ```

## Verification Steps

1. Run this command to verify all directories exist:
   ```bash
   find . -type d -name app -o -name prompts -o -name tests
   ```
   Should return the three main directories.

2. Count all Python package files:
   ```bash
   find . -name "__init__.py" | wc -l
   ```
   Should return 10 files.

3. Count placeholder modules:
   ```bash
   find app -type f -name "*.py" | grep -v "__init__" | wc -l
   ```
   Should return 8 files.

4. List full directory tree (optional, for review):
   ```bash
   tree -L 3 app/
   ```
   Or on Windows: `dir /s /b`

## Expected Output

A complete directory structure with:
- 8 subdirectories (api, core, db, models, repositories, services under app + prompts + tests)
- 10 `__init__.py` files
- 8 placeholder Python modules
- All directories are ready for code development

## Code Example

Create directories using Python if bash is not available:

```python
import os

directories = [
    'app/api',
    'app/core',
    'app/db',
    'app/models',
    'app/repositories',
    'app/services',
    'prompts',
    'tests/test_api',
    'tests/test_services',
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"Created: {directory}")
```

## Commit Message

```
feat(project): initialize project directory structure

Create complete directory hierarchy for FastAPI + LangChain application following Python best practices. Includes app packages, tests, and prompts folders with __init__.py files.
```

---

**Completion Time:** ~10 minutes
**Dependencies:** None
