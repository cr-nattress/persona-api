# Next.js Test App: Person Aggregate Root API

A lightweight Next.js application to test and verify the Person Aggregate Root API endpoints.

## Status

📋 **Plan Phase** - No implementation yet. See `PLAN.md` for detailed specification.

## Quick Summary

### Purpose

Test two critical user flows:

1. **Create New Person with Persona**
   - User uploads unstructured data
   - System creates a new person
   - System generates initial persona from data
   - Person appears in dropdown list

2. **Update Existing Person**
   - User selects person from dropdown
   - User submits new unstructured data
   - System regenerates persona with all accumulated data
   - Persona version increments

### Key Features

- **Person Selector**: Dropdown to choose which person to work with
- **Data Upload Form**: Accept unstructured text (up to 100KB)
- **Persona Display**: Show generated persona JSON with metadata
- **API Debug Panel**: Real-time logging of all API calls for troubleshooting

### Tech Stack

- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: TBD (Tailwind CSS recommended)
- **HTTP Client**: Native fetch API
- **State**: React hooks (useState, useEffect, useCallback)

## Project Structure

```
test-app/
├── package.json
├── tsconfig.json
├── next.config.js
├── .env.local.example
├── PLAN.md                    ← Detailed specification (803 lines)
├── README.md                  ← This file
├── public/
└── src/
    ├── app/
    │   ├── layout.tsx         # Root layout
    │   ├── page.tsx           # Main test page
    │   └── globals.css        # Styles
    ├── components/
    │   ├── PersonForm.tsx     # Data submission
    │   ├── PersonSelector.tsx # Person dropdown
    │   ├── PersonaDisplay.tsx # Persona viewer
    │   ├── ApiDebugPanel.tsx  # API call logger
    │   └── Loading.tsx        # Loading indicator
    ├── services/
    │   ├── api.ts             # API client
    │   ├── sanitizer.ts       # Input cleaning & escaping (NEW)
    │   └── types.ts           # TypeScript interfaces
    └── hooks/
        └── usePersons.ts      # Custom hook for persons management
```

## Components Planned

| Component | Purpose | Key Props |
|-----------|---------|-----------|
| **PersonSelector** | Person dropdown | `persons`, `selectedPersonId`, `onSelect`, `isLoading` |
| **PersonForm** | Data input form | `personId`, `isLoading`, `onSubmit` |
| **PersonaDisplay** | Persona viewer | `persona`, `personDataCount`, `isLoading` |
| **ApiDebugPanel** | API call logger | `calls`, `isOpen`, `onToggle` |
| **Loading** | Loading indicator | `isLoading`, `message` |

## API Endpoints Used

### Flow 1: Create New Person
```
POST   /v1/person                                    → Create person
POST   /v1/person/{id}/data-and-regenerate         → Add data + regenerate
GET    /v1/person                                  → Get persons list
```

### Flow 2: Update Existing Person
```
POST   /v1/person/{id}/data-and-regenerate         → Add data + regenerate
GET    /v1/person                                  → Refresh persons list
```

## Expected API Responses

### Create Person
```json
{
  "id": "uuid",
  "created_at": "2025-11-09T...",
  "updated_at": "2025-11-09T...",
  "person_data_count": 0,
  "latest_persona_version": null
}
```

### Add Data & Regenerate
```json
{
  "person_data": {
    "id": "uuid",
    "person_id": "uuid",
    "raw_text": "...",
    "source": "api",
    "created_at": "2025-11-09T..."
  },
  "persona": {
    "id": "uuid",
    "person_id": "uuid",
    "persona": { "name": "...", "summary": "..." },
    "version": 1,
    "computed_from_data_ids": ["uuid"],
    "created_at": "2025-11-09T..."
  }
}
```

### List Persons
```json
[
  {
    "id": "uuid",
    "created_at": "2025-11-09T...",
    "updated_at": "2025-11-09T...",
    "person_data_count": 1,
    "latest_persona_version": 1
  }
]
```

## Configuration

### Environment Variables

Create `.env.local`:
```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8080
```

## Page Layout

```
┌─────────────────────────────────┐
│  Person Aggregate Root API Test │
└─────────────────────────────────┘

┌─ Person Management ──────────────┐
│ Select: [▼ Choose person...] [+] │
└──────────────────────────────────┘

┌─ Data Submission ────────────────┐
│ [Large textarea for text]        │
│ Char count: 0 / 100,000         │
│ Source: [api ▼]                  │
│ [Submit] [Clear]                 │
└──────────────────────────────────┘

┌─ Generated Persona ──────────────┐
│ (Shows persona JSON & metadata)  │
│ Version: 1                       │
│ Created: [timestamp]             │
│ [Copy JSON] [Refresh]            │
└──────────────────────────────────┘

┌─ Debug Panel [▼] ────────────────┐
│ (3 API calls)                    │
│ [POST] /v1/person 201ms         │
│ [POST] /v1/person/.../data 3.2s │
│ [GET] /v1/person 142ms          │
│ [Copy All] [Clear]              │
└──────────────────────────────────┘
```

## Input Sanitization (CRITICAL)

The UI **MUST** clean and escape all user input to prevent API failures.

### What Gets Sanitized

| Input | Treatment | Example |
|-------|-----------|---------|
| Whitespace | Trim & collapse | "Hello    world" → "Hello world" |
| Line breaks | Normalize | "A\r\nB" → "A\nB" |
| Control chars | Remove | "Text\x00here" → "Texthere" |
| Zero-width chars | Remove | "Zero​width" → "Zerowidth" |
| Emoji | Preserve | "Hi 👋" → "Hi 👋" |
| Special chars | Preserve | "He said \"hi!\"" → Preserved |
| Null bytes | Remove | "Null\0byte" → "Nullbyte" |

### Sanitization Process

1. **Remove dangerous characters**
   - Null bytes (\0)
   - Control characters (ASCII 0-31 except \n, \r, \t)
   - Zero-width characters (U+200B, U+200C, etc.)

2. **Normalize whitespace**
   - Collapse multiple spaces to single space
   - Convert \r\n to \n
   - Preserve intentional line breaks

3. **Validate encoding**
   - Ensure UTF-8 validity
   - Reject malformed sequences
   - Handle emoji safely

4. **Enforce limits**
   - Check ≤ 100,000 bytes (after UTF-8 encoding)
   - Reject empty input
   - Display byte count to user

### Implementation

Use `sanitizeRawText()` function (provided in sanitizer.ts):

```typescript
import { sanitizeRawText, validateSanitizedInput } from '@/services/sanitizer';

// On user input
const cleaned = sanitizeRawText(userInput);

// Before submitting
const { valid, error } = validateSanitizedInput(cleaned);
if (!valid) {
  showError(error); // e.g., "Text exceeds 100,000 byte limit"
  return;
}

// Send to API
await addPersonData(personId, cleaned, source);
```

### Validation Rules

- **raw_text**: Required, 1-100,000 bytes (after sanitization)
- **source**: Required, select from dropdown
- **person_id**: Required, must select or create person
- **encoding**: Must be valid UTF-8

### Error Messages

- "Text cannot be empty"
- "Text exceeds 100,000 byte limit (current: X bytes)"
- "Invalid characters detected in input"
- "Text encoding error - please try again"

### API Error Handling
- **Network error**: "Unable to connect to API"
- **4xx error**: "Invalid request: {details}"
- **5xx error**: "Server error, please try again"
- **Timeout**: "Request timed out"

## Testing Scenarios

✅ **Scenario 1: Create New Person**
- Create person
- Submit data
- Verify persona generates (v1)
- Check dropdown shows new person
- Debug panel logs all calls

✅ **Scenario 2: Update Existing Person**
- Select person from dropdown
- Submit new data
- Verify persona regenerates (v2)
- Check version incremented
- Debug panel shows new call

✅ **Scenario 3: Large Data**
- Submit 50KB text (valid)
- Try 101KB (rejected with error)

✅ **Scenario 4: Multiple Persons**
- Create 3 persons
- Switch between them
- Each shows correct data/persona

✅ **Scenario 5: Error Recovery**
- Disconnect API
- See error message
- Reconnect and retry

## Implementation Phases

1. **Setup**: Next.js, TypeScript, environment
2. **API Client**: `services/api.ts` + types
3. **State Management**: Custom hooks
4. **Components**: PersonSelector, PersonForm, PersonaDisplay, ApiDebugPanel
5. **Main Page**: Integration and wiring
6. **Polish**: Styling, error handling, accessibility

## Success Criteria

✅ Both user flows work end-to-end
✅ Persons dropdown functional
✅ Debug panel shows all API calls
✅ Error handling works properly
✅ UI is responsive and intuitive

## Notes

- This is a test/demo application, not production code
- Focus on functionality over perfection
- Can use simple CSS or Tailwind CSS
- No complex state library needed (React hooks sufficient)
- Keep components simple and reusable
- Prioritize debuggability for API verification

## Getting Started (Placeholder)

Implementation instructions will be provided in next phase.

## Related Documentation

- `PLAN.md` - Complete 800+ line specification (READ THIS FIRST)
- `../IMPLEMENTATION-PLAN.md` - Person Aggregate Root API design
- `../docs/DEPLOYMENT_GUIDE.md` - API deployment guide

---

**Status**: 📋 Plan Complete → Ready for implementation
