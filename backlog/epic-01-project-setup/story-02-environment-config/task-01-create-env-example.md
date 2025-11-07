# TASK-01-02-01: Create .env.example File

**Story:** US-01-02

**Estimated Time:** 5 minutes

**Description:** Create .env.example file with all required environment variables documented.

## Agent Prompt

You are implementing **EPIC-01: Project Setup & Infrastructure**.

**Goal:** Create a .env.example file documenting all environment variables needed for the Persona-API.

**Context:** The .env.example file serves as documentation and a template for developers. It shows what environment variables are needed without exposing actual values.

**Instructions:**

1. Create `.env.example` at the project root with the following content:

```
# OpenAI API Configuration
# Get your key from: https://platform.openai.com/account/api-keys
OPENAI_API_KEY=sk-your-api-key-here

# Supabase Database Configuration
# Get these from: https://app.supabase.com/project/[your-project]/settings/api
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here

# Application Configuration
ENVIRONMENT=development
# Options: development, staging, production
# development: verbose logging, debug mode enabled
# staging: minimal logging, error tracking enabled
# production: errors only, optimized performance

LOG_LEVEL=DEBUG
# Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

2. Add clear comments explaining each variable's purpose and where to find the values.

3. Ensure no actual secrets are in this file (use placeholder values).

## Verification Steps

1. Verify file exists:
   ```bash
   ls -la .env.example
   ```

2. Verify content is readable:
   ```bash
   cat .env.example
   ```

3. Verify no real secrets are present:
   ```bash
   grep -i "actual\|real\|secret\|password" .env.example
   ```
   Should return nothing.

## Expected Output

A .env.example file with:
- All required environment variables
- Clear descriptions and comments
- Placeholder values (no real secrets)
- Links to documentation where applicable

## Commit Message

```
docs(.env.example): add environment configuration template

Create .env.example with all required environment variables for OpenAI, Supabase, and application configuration.
```

---

**Completion Time:** ~5 minutes
**Dependencies:** None
