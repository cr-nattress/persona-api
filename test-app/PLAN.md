# Test App Plan: Person Aggregate Root API Verification

**Objective**: Build a simple Next.js test application to verify core user flows of the Person Aggregate Root API.

**Status**: Plan Phase (No Implementation)

---

## Overview

A lightweight Next.js application that demonstrates and verifies two critical user flows:

1. **Create New Person with Persona**: Upload unstructured data → Person created → Persona generated
2. **Update Existing Person**: Select person from list → Submit new data → Persona regenerated

The app includes real-time API call debugging for development and troubleshooting.

---

## Requirements

### Functional Requirements

#### User Flow 1: Create New Person with Persona
```
User uploads raw text
  ↓
App creates new person (POST /v1/person)
  ↓
App adds data submission (POST /v1/person/{id}/data-and-regenerate)
  ↓
App displays created persona
  ↓
Person is added to dropdown list
```

**Success Criteria:**
- Person is created with UUID
- Data is stored with source="api"
- Persona is generated (version 1)
- UI shows persona JSON output
- Person appears in dropdown

#### User Flow 2: Update Existing Person with New Data
```
User selects person from dropdown
  ↓
User uploads new raw text
  ↓
App adds data submission (POST /v1/person/{id}/data-and-regenerate)
  ↓
App displays updated persona with new version
  ↓
Persona version number increments
```

**Success Criteria:**
- Persona version increments
- New data is appended to history
- Old data still exists
- Persona reflects combined context

### Non-Functional Requirements

- **API Base URL**: Configurable (default: http://localhost:8080)
- **Person List**: Auto-refreshes after each operation
- **Error Handling**: Display API errors clearly
- **Debug Panel**: Real-time, scrollable, copyable
- **Performance**: <5s response time for API calls
- **Responsive**: Works on desktop and tablet

---

## Technology Stack

### Frontend
- **Framework**: Next.js 14+ (App Router)
- **UI Components**: React + TypeScript
- **Styling**: Tailwind CSS (or plain CSS)
- **HTTP Client**: fetch API (built-in) or Axios
- **State Management**: React hooks (useState, useEffect, useCallback)
- **Validation**: Basic client-side validation

### Dev Tools
- **Package Manager**: npm or pnpm
- **Build Tool**: Next.js built-in
- **Environment**: Node.js 18+

### Directory Structure
```
test-app/
├── package.json
├── tsconfig.json
├── next.config.js
├── .env.local (git-ignored)
├── public/
│   └── favicon.ico
├── src/
│   ├── app/
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Main test page
│   │   └── globals.css         # Global styles
│   ├── components/
│   │   ├── PersonForm.tsx      # Data submission form (with sanitization)
│   │   ├── PersonSelector.tsx  # Person dropdown
│   │   ├── PersonaDisplay.tsx  # Persona JSON viewer
│   │   ├── ApiDebugPanel.tsx   # Debug panel
│   │   └── Loading.tsx         # Loading indicator
│   ├── services/
│   │   ├── api.ts              # API client functions
│   │   ├── sanitizer.ts        # Input cleaning & escaping (NEW)
│   │   └── types.ts            # TypeScript interfaces
│   └── hooks/
│       └── usePersons.ts        # Custom hook for persons list
├── .env.local.example
└── README.md
```

---

## Component Architecture

### 1. **Main Page** (`src/app/page.tsx`)
**Responsibility**: Orchestrate the test application

**Features:**
- Display title and description
- Render all sub-components
- Manage global state (persons list, current persona, etc.)
- Handle loading/error states
- Layout and spacing

**State:**
```typescript
- persons: Person[] // List of all persons
- selectedPersonId: UUID | null
- currentPersona: Persona | null
- isLoading: boolean
- error: string | null
- apiCalls: ApiCall[] // Debug panel data
```

**Props**: None (root component)

---

### 2. **PersonSelector Component** (`src/components/PersonSelector.tsx`)
**Responsibility**: Display dropdown of available persons

**Props:**
```typescript
{
  persons: Person[];
  selectedPersonId: UUID | null;
  onSelect: (personId: UUID) => void;
  isLoading: boolean;
}
```

**Features:**
- Dropdown/select element with all persons
- Shows person IDs and creation dates
- "Create New Person" option
- Disabled state when loading
- Clear selection button

**Behavior:**
- Trigger parent callback when person selected
- Display "No persons" message if list empty
- Auto-select first person when list changes (optional)

---

### 3. **PersonForm Component** (`src/components/PersonForm.tsx`)
**Responsibility**: Accept unstructured data input and submit

**Props:**
```typescript
{
  personId: UUID | null;
  isLoading: boolean;
  onSubmit: (data: { rawText: string; source: string }) => void;
}
```

**Features:**
- Large textarea for raw_text input
- Source selector dropdown (api, import, manual, etc.)
- Submit button
- Character counter (0 - 100,000)
- Validation feedback
- Disabled when no person selected or loading

**Behavior:**
- Validate raw_text is not empty and within limits
- Validate person is selected
- Disable submit while loading
- Clear form after successful submission
- Show error messages

**Validation & Sanitization:**
```
- raw_text: required, min 1 char, max 100,000 chars
- source: required, select from predefined list
- personId: required (selected person)
```

**Input Sanitization (CRITICAL):**

The form MUST clean and escape user input to prevent API call failures:

1. **Whitespace Handling:**
   - Trim leading/trailing whitespace
   - Collapse multiple consecutive whitespace characters to single space
   - Preserve intentional line breaks (convert \r\n to \n, normalize)

2. **Character Encoding:**
   - Ensure all input is UTF-8 encoded
   - Remove or escape non-printable characters (control chars, null bytes)
   - Remove zero-width characters (zero-width joiner, zero-width space, etc.)

3. **Special Characters:**
   - Do NOT remove special characters (they are valid in unstructured data)
   - Properly escape quotes, backslashes for JSON transmission
   - Handle emoji and unicode characters safely

4. **Invalid Sequences:**
   - Remove orphaned Unicode surrogates
   - Fix malformed UTF-8 sequences
   - Strip invalid XML/JSON control characters

5. **Payload Integrity:**
   - Validate final string is valid UTF-8
   - Check string doesn't exceed 100,000 bytes (after encoding)
   - Ensure no corruption from previous transformations

**Sanitization Implementation Strategy:**

```typescript
function sanitizeRawText(input: string): string {
  // 1. Handle null/undefined
  if (!input) return '';

  // 2. Ensure UTF-8 and remove null bytes
  input = input.replace(/\0/g, '');

  // 3. Remove control characters except whitespace and newlines
  // Keep: \t (tab), \n (newline), \r (carriage return), regular spaces
  input = input.replace(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/g, '');

  // 4. Remove zero-width characters
  input = input.replace(/[\u200B\u200C\u200D\u200E\u200F\uFEFF]/g, '');

  // 5. Normalize line endings: \r\n -> \n, \r -> \n
  input = input.replace(/\r\n/g, '\n').replace(/\r/g, '\n');

  // 6. Fix excessive whitespace (collapse multiple spaces, trim)
  input = input.split('\n').map(line => {
    // Collapse multiple spaces to single space on each line
    return line.replace(/[ \t]+/g, ' ').trim();
  }).join('\n');

  // 7. Remove leading/trailing whitespace from entire string
  input = input.trim();

  // 8. Remove excessive blank lines (more than 2 consecutive)
  input = input.replace(/\n\n\n+/g, '\n\n');

  // 9. Final validation: ensure valid UTF-8
  try {
    new TextEncoder().encode(input);
  } catch {
    return ''; // Invalid UTF-8, reject
  }

  return input;
}

function validateSanitizedInput(input: string): { valid: boolean; error?: string } {
  if (!input || input.length === 0) {
    return { valid: false, error: 'Text cannot be empty' };
  }

  const byteLength = new TextEncoder().encode(input).length;

  if (byteLength > 100000) {
    return {
      valid: false,
      error: `Text exceeds limit: ${byteLength} bytes (max 100,000)`
    };
  }

  return { valid: true };
}
```

**Usage in PersonForm Component:**

```typescript
const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
  const sanitized = sanitizeRawText(e.target.value);
  const validation = validateSanitizedInput(sanitized);

  setRawText(sanitized);

  if (!validation.valid) {
    setError(validation.error);
  } else {
    setError(null);
  }

  // Update character counter with byte length
  setCharCount(new TextEncoder().encode(sanitized).length);
};

const handleSubmit = async () => {
  const validation = validateSanitizedInput(rawText);

  if (!validation.valid) {
    setError(validation.error);
    return;
  }

  // Sanitized rawText is ready for API call
  await onSubmit({ rawText, source });
};
```

**What Gets Sanitized:**

| Input Type | Treatment | Example |
|-----------|-----------|---------|
| Normal text | Preserved | "Hello world" → "Hello world" |
| Multiple spaces | Collapsed | "Hello    world" → "Hello world" |
| Line breaks | Normalized | "Line1\r\nLine2" → "Line1\nLine2" |
| Tabs | Preserved | "Tab\there" → "Tab here" (collapsed) |
| Emoji | Preserved | "Hello 👋 world" → "Hello 👋 world" |
| Special chars | Preserved | "He said: \"hi!\"" → "He said: \"hi!\"" |
| Control chars | Removed | "Text\x00here" → "Texthere" |
| Zero-width chars | Removed | "Zero​width" → "Zerowidth" |
| Excessive newlines | Collapsed | "Line1\n\n\nLine2" → "Line1\n\nLine2" |
| Null bytes | Removed | "Null\0byte" → "Nullbyte" |

**Error Messages to Display:**

- "Text cannot be empty"
- "Text exceeds 100,000 character limit (current: X bytes)"
- "Invalid characters detected in input"
- "Text encoding error - please try again"

---

### 4. **PersonaDisplay Component** (`src/components/PersonaDisplay.tsx`)
**Responsibility**: Display generated persona with metadata

**Props:**
```typescript
{
  persona: Persona | null;
  personDataCount: number;
  isLoading: boolean;
}
```

**Features:**
- Display persona JSON in formatted, readable way
- Show metadata:
  - Persona ID
  - Version number
  - Created/Updated timestamps
  - Data submissions used (count)
- "Copy JSON" button
- "Refresh" button
- Collapse/expand sections
- Loading spinner while fetching

**Layout:**
```
┌─ Persona Information ──────────────────┐
│ ID: [uuid]                             │
│ Version: 2                             │
│ Created: [timestamp]                   │
│ Updated: [timestamp]                   │
│ Data Submissions: 3                    │
└────────────────────────────────────────┘

┌─ Persona JSON ─────────────────────────┐
│ {                                      │
│   "name": "...",                       │
│   "summary": "...",                    │
│   ...                                  │
│ }                                      │
│ [Copy] [Refresh]                       │
└────────────────────────────────────────┘
```

---

### 5. **ApiDebugPanel Component** (`src/components/ApiDebugPanel.tsx`)
**Responsibility**: Display all API calls for debugging

**Props:**
```typescript
{
  calls: ApiCall[];
  isOpen: boolean;
  onToggle: () => void;
}
```

**Features:**
- Collapsible panel (can be hidden to save space)
- List of all API calls made during session
- For each call:
  - Method (GET, POST, DELETE)
  - Endpoint URL
  - Timestamp
  - Request body (JSON, if applicable)
  - Response status code
  - Response body (JSON, if applicable)
  - Duration (ms)
- Color-coded status codes:
  - 2xx: Green
  - 4xx: Yellow
  - 5xx: Red
- "Copy All" button
- "Clear" button
- Scroll area with max height
- Search/filter capability (optional)

**Data Structure:**
```typescript
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
  duration: number; // milliseconds
  error?: string;
}
```

**Example Display:**
```
[▼] Debug Panel (12 calls)

1. [14:32:15] POST /v1/person
   Status: 201 | Duration: 245ms
   Response: {"id": "uuid-1", ...}

2. [14:32:16] POST /v1/person/uuid-1/data-and-regenerate
   Status: 201 | Duration: 3421ms
   Response: {"person_data": {...}, "persona": {...}}

3. [14:32:45] GET /v1/person
   Status: 200 | Duration: 142ms
   Response: [{...}, {...}]

[Copy All] [Clear]
```

---

### 6. **Loading Component** (`src/components/Loading.tsx`)
**Responsibility**: Display loading indicator

**Props:**
```typescript
{
  isLoading: boolean;
  message?: string;
}
```

**Features:**
- Simple spinner animation
- Optional loading message
- Overlay style (optional)
- Dismissible (optional)

---

## Service Layer

### Sanitization Service (`src/services/sanitizer.ts`)

**New module for input cleaning and validation**

**Functions:**

#### 1. `sanitizeRawText(input: string): string`
Cleans user input to prevent API failures:
- Removes null bytes and control characters
- Removes zero-width characters
- Normalizes line endings
- Collapses excessive whitespace
- Validates UTF-8 encoding

#### 2. `validateSanitizedInput(input: string): { valid: boolean; error?: string }`
Validates sanitized input against constraints:
- Checks minimum length (>0)
- Checks maximum length (≤100,000 bytes)
- Returns specific error messages for debugging

#### 3. `escapeForJson(input: string): string`
Escapes special characters for safe JSON transmission:
- Handles quotes, backslashes, newlines
- Maintains unicode characters
- Ensures valid JSON string encoding

---

### API Client Service (`src/services/api.ts`)

**Note**: All API functions receive pre-sanitized input from components.
Input should always be sanitized using `sanitizeRawText()` before calling API.

**Functions:**

#### 1. `createPerson(): Promise<Person>`
```typescript
POST /v1/person
Returns: Person (id, created_at, updated_at, person_data_count, latest_persona_version)
```

#### 2. `listPersons(limit?: number, offset?: number): Promise<Person[]>`
```typescript
GET /v1/person?limit=50&offset=0
Returns: Person[]
```

#### 3. `addPersonDataAndRegenerate(personId: UUID, rawText: string, source: string): Promise<{ person_data: PersonData, persona: Persona }>`
```typescript
POST /v1/person/{personId}/data-and-regenerate?raw_text={text}&source={source}
Returns: { person_data, persona }
```

#### 4. `getPersona(personId: UUID): Promise<Persona>`
```typescript
GET /v1/person/{personId}/persona
Returns: Persona (id, person_id, persona, version, computed_from_data_ids, etc.)
```

#### 5. `getPersonDataHistory(personId: UUID, limit?: number, offset?: number): Promise<{ items: PersonData[], total: number }>`
```typescript
GET /v1/person/{personId}/data?limit=50&offset=0
Returns: { items, total, limit, offset }
```

**Implementation Details:**
- All functions log API calls to a global registry
- Each call recorded with method, endpoint, timestamp, request, response, duration
- Error handling: wrap errors and pass to component
- Base URL from environment variable `NEXT_PUBLIC_API_BASE_URL`
- Automatic JSON serialization/deserialization

---

## Type Definitions (`src/services/types.ts`)

```typescript
// From API responses
interface Person {
  id: UUID;
  created_at: string; // ISO timestamp
  updated_at: string;
  person_data_count: number;
  latest_persona_version: number | null;
}

interface PersonData {
  id: UUID;
  person_id: UUID;
  raw_text: string;
  source: string;
  created_at: string;
  updated_at: string;
}

interface Persona {
  id: UUID;
  person_id: UUID;
  persona: Record<string, unknown>; // JSON object
  version: number;
  computed_from_data_ids: UUID[];
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

type UUID = string;
```

---

## Custom Hooks

### `usePersons` Hook (`src/hooks/usePersons.ts`)

**Purpose**: Manage persons list state and refresh logic

**Functions:**
- `persons: Person[]` - Current list of persons
- `isLoading: boolean` - Loading state
- `error: string | null` - Error message
- `refreshPersons(): Promise<void>` - Fetch latest list
- `addNewPerson(): Promise<Person>` - Create new person and add to list

**Usage:**
```typescript
const { persons, isLoading, error, refreshPersons, addNewPerson } = usePersons();
```

---

## User Interaction Flow

### Flow 1: Create New Person with Persona

```
1. User sees empty PersonSelector dropdown
2. User clicks "Create New Person" (or "+" button)
   → Calls createPerson() API
   → New person added to dropdown
   → Person auto-selected in dropdown

3. User enters unstructured data in PersonForm
   - E.g., "John is a software engineer with 10 years experience..."

4. User selects source (defaults to "api")

5. User clicks "Submit" button
   → Calls addPersonDataAndRegenerate() API
   → Shows loading indicator
   → ApiDebugPanel logs the call

6. Response received:
   → PersonaDisplay shows generated persona (version 1)
   → Person's data_count shows "1"
   → Debug panel shows both request/response

7. Persons list auto-refreshes:
   → Dropdown shows updated person with latest_persona_version="1"
```

**API Calls Made:**
1. POST /v1/person → Create person
2. POST /v1/person/{id}/data-and-regenerate → Add data + regenerate
3. GET /v1/person → Refresh persons list

### Flow 2: Update Existing Person

```
1. User selects person from dropdown
   → Shows that person's current persona (if exists)
   → PersonForm becomes enabled

2. User enters new unstructured data
   - E.g., "John now has 12 years experience and leads a team..."

3. User clicks "Submit" button
   → Calls addPersonDataAndRegenerate() API
   → Shows loading indicator

4. Response received:
   → PersonaDisplay updates with new persona
   → Version number increments (1 → 2)
   → Shows timestamp updated
   → ApiDebugPanel logs the call

5. Data history verified:
   → User can see both old and new submissions
   → Persona shows both were used in computation
```

**API Calls Made:**
1. POST /v1/person/{id}/data-and-regenerate → Add data + regenerate
2. GET /v1/person → Refresh persons list

---

## Page Layout & UI Structure

```
┌─────────────────────────────────────────────────────────────┐
│ Person Aggregate Root API Test                              │
│ Test the new person management and persona generation flows │
└─────────────────────────────────────────────────────────────┘

┌─ Person Management ─────────────────────────────────────────┐
│                                                              │
│  Select Person: [▼ Choose a person...              [+ New]   │
│                                                              │
│  Or create new by uploading data below                      │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌─ Data Submission ──────────────────────────────────────────┐
│ Paste unstructured data about the person:                  │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │                                                         │ │
│ │ [Large textarea for raw text input]                   │ │
│ │                                                         │ │
│ │ Character count: 245 / 100,000                        │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ Source: [api ▼]  [Submit] [Clear]                          │
│                                                             │
│ ⏳ Loading... (if processing)                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─ Generated Persona ─────────────────────────────────────────┐
│                                                              │
│ No persona yet. Create a person or submit data.             │
│                                                              │
│ (Once generated, will show version, created_at, JSON)      │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌─ Debug Panel [▼] ─────────────────────────────────────────┐
│ (3 API calls logged)                                       │
│                                                             │
│ [POST] /v1/person                 201 | 245ms | 14:32:15   │
│ └─ Response: {"id": "uuid-1", ...}                         │
│                                                             │
│ [POST] /v1/person/.../data-and-regenerate 201 | 3421ms    │
│ └─ Response: {"person_data": {...}, "persona": {...}}      │
│                                                             │
│ [GET] /v1/person                  200 | 142ms | 14:32:16   │
│ └─ Response: [...]                                         │
│                                                             │
│ [Copy All] [Clear]                                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Environment Configuration

### `.env.local` (Git-ignored)
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8080
```

### `.env.local.example` (Committed)
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8080
```

---

## Error Handling Strategy

### API Errors
- **Network Error**: Display "Unable to connect to API"
- **4xx Response**: Display "Invalid request: {error message}"
- **5xx Response**: Display "Server error: please try again"
- **Timeout**: Display "Request timed out"

### Form Validation Errors
- **Empty raw_text**: "Please enter some data"
- **Too long raw_text**: "Text exceeds 100,000 character limit"
- **No person selected**: "Please select or create a person"

### Display Strategy
- Toast/modal notifications for transient errors
- Inline error messages for form validation
- Full error details in debug panel

---

## Testing Scenarios

### Scenario 1: Happy Path - Create & Regenerate
```
✓ Create new person
✓ Submit data with source="api"
✓ Persona generates version 1
✓ Person appears in dropdown
✓ All API calls logged in debug panel
✓ Response JSON is valid
```

### Scenario 2: Update Existing Person
```
✓ Select existing person from dropdown
✓ Submit new data
✓ Persona version increments to 2
✓ Timestamp updates
✓ Data history shows both submissions
✓ All API calls logged
```

### Scenario 3: Large Text Submission
```
✓ Submit 50KB text (valid)
✓ Submit 101KB text (rejected)
✓ Error message displayed correctly
```

### Scenario 4: Multiple Persons
```
✓ Create person 1 with data
✓ Create person 2 with data
✓ Switch between persons in dropdown
✓ Each shows its own persona and data count
✓ No cross-contamination
```

### Scenario 5: Error Handling
```
✓ API unreachable → error displayed
✓ Invalid request → error details shown
✓ Server error → graceful message shown
✓ Debug panel shows all failed requests
```

---

## Performance Considerations

### Optimization Goals
- Initial page load: <2 seconds
- API response display: <500ms
- Smooth UI interactions

### Strategies
- Minimal dependencies
- Lazy load debug panel (hidden by default)
- No unnecessary re-renders (React.memo for components)
- Client-side pagination (if persona has many versions)
- Debounce character counter (optional)

---

## Accessibility (Nice-to-Have)

- Semantic HTML (button, form, select, textarea)
- ARIA labels for form fields
- Keyboard navigation support
- Color contrast for readability
- Loading state announcements

---

## File Checklist (Before Implementation)

- [ ] Understand all API endpoints and responses
- [ ] Review TypeScript types from API docs
- [ ] Plan component prop interfaces
- [ ] Design API error handling strategy
- [ ] Decide on styling approach (Tailwind vs CSS modules)
- [ ] Plan state management approach
- [ ] Test API manually first (curl, Postman)
- [ ] Set up Next.js project structure
- [ ] Configure TypeScript compiler options

---

## Implementation Order (Recommended)

1. **Setup** (Phase 0)
   - Initialize Next.js project
   - Install dependencies
   - Configure environment variables
   - Set up TypeScript

2. **Core API Client** (Phase 1)
   - Implement `src/services/api.ts`
   - Implement `src/services/types.ts`
   - Test API calls manually

3. **State Management** (Phase 2)
   - Implement `src/hooks/usePersons.ts`
   - Set up API logging registry

4. **Components** (Phase 3)
   - PersonSelector
   - PersonForm
   - PersonaDisplay
   - ApiDebugPanel
   - Loading

5. **Main Page** (Phase 4)
   - Integrate all components
   - Wire up state and callbacks
   - Test both user flows

6. **Polish** (Phase 5)
   - Error handling refinement
   - Styling and layout
   - Accessibility improvements
   - Documentation

---

## Success Criteria

✅ **Both user flows work end-to-end:**
- Create new person → Submit data → Persona generated
- Select person → Submit new data → Persona regenerated with incremented version

✅ **Persons dropdown populated and functional:**
- Shows all persons
- Can select and update
- Auto-refreshes after operations

✅ **Debug panel shows all API calls:**
- Correct methods and endpoints
- Request/response bodies visible
- Status codes and timing displayed
- Can copy all for troubleshooting

✅ **Error handling works:**
- API errors displayed clearly
- Form validation prevents invalid submission
- Network errors handled gracefully

✅ **UI is responsive and intuitive:**
- Clear user guidance
- Loading states visible
- Success feedback provided
- No confusing states

---

## Notes

- This is a test/demo app, not production code
- Focus on functionality over perfection
- Can be simple CSS or Tailwind
- No complex state management library needed
- Keep components minimal and focused
- Prioritize clarity and debuggability

---

## Questions to Answer Before Implementation

1. Should persons list auto-refresh on page load?
2. Should persona auto-select the latest when dropdown changes?
3. Should form auto-clear after successful submission?
4. Should debug panel be expanded or collapsed by default?
5. How many personas should be shown in persona history (optional feature)?
6. Should there be a "refresh all" button to re-fetch everything?
7. Should API calls older than X minutes be auto-removed from debug panel?
8. Should there be a "test data" button to pre-fill the form?

---

**Plan Complete** - Ready for implementation phase.
