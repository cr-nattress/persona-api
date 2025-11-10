# EPIC-02: Service Layer

## Epic Overview

**Epic ID**: EPIC-02
**Epic Name**: Service Layer
**Epic Owner**: Development Team
**Status**: Pending
**Story Points**: 15
**Priority**: High (Critical infrastructure)

## Business Value Statement

Implement core service layer components including input sanitization, API client functions, and custom React hooks to provide a robust foundation for UI components and ensure reliable API communication.

**Business Impact**: These services are critical infrastructure that prevents API failures, handles data sanitization, and provides reusable state management patterns.

## Current State vs Target State

### Current State
- No input sanitization exists (risk of API failures)
- No API client functions implemented
- No state management hooks available
- Components cannot communicate with API

### Target State
- Input sanitization service prevents malformed API requests
- Complete API client with all required endpoints
- API call logging system operational for debugging
- Custom hooks provide reusable state management
- All TypeScript types defined for API responses
- Unit tests validate sanitization logic

## Technical Approach

### Services to Implement

1. **Sanitizer Service** (`src/services/sanitizer.ts`)
   - Clean user input before API submission
   - Validate against constraints (0-100,000 bytes)
   - Handle UTF-8 encoding, control characters, whitespace

2. **API Client** (`src/services/api.ts`)
   - HTTP functions for all Person API endpoints
   - Automatic logging of requests/responses
   - Error handling and timeout management
   - Type-safe interfaces

3. **Type Definitions** (`src/services/types.ts`)
   - Person, PersonData, Persona interfaces
   - ApiCall logging structure
   - Request/response types

4. **Custom Hooks** (`src/hooks/usePersons.ts`)
   - Persons list state management
   - CRUD operations (create, list, refresh)
   - Loading and error states

## User Stories

This epic contains the following user stories:

### Story 01: Input Sanitization (5 points)
**As a** developer
**I want** to implement input sanitization functions
**So that** user input is cleaned before API submission

**Tasks**:
1. Create sanitizer service with type definitions
2. Implement sanitization and validation functions
3. Write unit tests for sanitization

### Story 02: API Client (5 points)
**As a** developer
**I want** to implement API client functions
**So that** components can communicate with the Person API

**Tasks**:
1. Create API types (Person, PersonData, Persona)
2. Implement API client functions
3. Setup API call logging

### Story 03: Custom Hooks (5 points)
**As a** developer
**I want** to create custom React hooks
**So that** state management is reusable and clean

**Tasks**:
1. Implement usePersons hook with CRUD operations

## Acceptance Criteria

The epic is considered complete when:

1. **Sanitization Service**:
   - Removes control characters and null bytes
   - Normalizes whitespace and line endings
   - Validates UTF-8 encoding
   - Enforces 100,000 byte limit
   - Returns clear error messages

2. **API Client**:
   - `createPerson()` function works
   - `listPersons()` function works
   - `addPersonDataAndRegenerate()` function works
   - `getPersona()` function works
   - All API calls logged to registry
   - Errors handled gracefully

3. **Type Definitions**:
   - All interfaces match API responses
   - No `any` types used
   - TypeScript compiles without errors

4. **Custom Hooks**:
   - `usePersons` manages persons list state
   - Provides create and refresh functions
   - Handles loading and error states
   - Re-renders components correctly

5. **Testing**:
   - Sanitization unit tests pass
   - All edge cases covered

## Definition of Done

- [ ] All user stories completed and accepted
- [ ] All acceptance criteria met
- [ ] TypeScript compiles without errors
- [ ] Unit tests written and passing
- [ ] No ESLint warnings
- [ ] Code reviewed and approved
- [ ] Documentation comments added to all functions
- [ ] Integration tested with mock data
- [ ] Code committed to version control

## Dependencies

### Blocks
- **EPIC-03**: UI Components (components need services)
- **EPIC-04**: Integration (main page needs hooks)

### Depends On
- **EPIC-01**: Project Setup (requires project structure)

## Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Sanitization misses edge cases | High | Medium | Comprehensive unit tests, reference SANITIZATION.md |
| API endpoint changes | High | Low | Document API contract, use TypeScript types |
| CORS issues in browser | Medium | Medium | Configure API for CORS, document in README |
| Hooks cause infinite re-renders | Medium | Low | Use useCallback, useMemo properly, test thoroughly |
| API timeout too short | Low | Medium | Make timeout configurable, default to 30s |

## Technical Notes

### Sanitization Functions

```typescript
// Remove dangerous characters, normalize whitespace
function sanitizeRawText(input: string): string

// Validate against constraints
function validateSanitizedInput(input: string): {
  valid: boolean;
  error?: string;
  byteLength?: number;
}

// Get UTF-8 byte length
function getByteLength(input: string): number
```

### API Client Functions

```typescript
// Create new person
async function createPerson(): Promise<Person>

// List all persons
async function listPersons(limit?: number, offset?: number): Promise<Person[]>

// Add data and regenerate persona
async function addPersonDataAndRegenerate(
  personId: string,
  rawText: string,
  source: string
): Promise<{ person_data: PersonData; persona: Persona }>

// Get latest persona
async function getPersona(personId: string): Promise<Persona>
```

### Type Definitions

```typescript
interface Person {
  id: string;
  created_at: string;
  updated_at: string;
  person_data_count: number;
  latest_persona_version: number | null;
}

interface PersonData {
  id: string;
  person_id: string;
  raw_text: string;
  source: string;
  created_at: string;
  updated_at: string;
}

interface Persona {
  id: string;
  person_id: string;
  persona: Record<string, unknown>;
  version: number;
  computed_from_data_ids: string[];
  created_at: string;
  updated_at: string;
}

interface ApiCall {
  id: string;
  method: 'GET' | 'POST' | 'DELETE';
  endpoint: string;
  timestamp: Date;
  request: {
    body?: unknown;
    params?: Record<string, unknown>;
  };
  response: {
    status: number;
    body: unknown;
  };
  duration: number;
  error?: string;
}
```

### Custom Hook Pattern

```typescript
function usePersons() {
  const [persons, setPersons] = useState<Person[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refreshPersons = useCallback(async () => {
    // Fetch persons from API
  }, []);

  const addNewPerson = useCallback(async () => {
    // Create new person
  }, []);

  return { persons, isLoading, error, refreshPersons, addNewPerson };
}
```

## Estimated Timeline

- **Story 01**: 45 minutes (3 tasks)
- **Story 02**: 45 minutes (3 tasks)
- **Story 03**: 20 minutes (1 task)
- **Total**: ~110 minutes

## Parallelization Opportunities

- **Story 01** and **Story 02** can be developed in parallel by different developers
- **Story 03** depends on Story 02 completion (needs API client)

## Success Metrics

- Sanitization catches 100% of known problematic inputs
- API client has <100ms overhead per call
- Hooks cause zero unnecessary re-renders
- TypeScript provides full autocomplete for all functions
- Zero runtime type errors

## Related Documentation

- `test-app/PLAN.md` - Lines 491-637 (Service Layer & Types)
- `test-app/SANITIZATION.md` - Complete sanitization guide
- `test-app/README.md` - Lines 189-244 (Sanitization summary)

## Epic Progress

- [ ] Story 01: Input Sanitization (0/3 tasks)
- [ ] Story 02: API Client (0/3 tasks)
- [ ] Story 03: Custom Hooks (0/1 tasks)

**Overall Progress**: 0% (0/7 tasks completed)

---

**Epic Created**: 2025-11-09
**Epic Status**: Ready for Execution
**Next Action**: Begin Story 01, Task 01 (Create sanitizer service)
