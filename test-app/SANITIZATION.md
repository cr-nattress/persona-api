# Input Sanitization & Escaping Strategy

## Overview

The Next.js test app **MUST** clean and escape all user input to prevent API call failures. This document details exactly what needs to be sanitized, why, and how to implement it.

## Why Sanitization Matters

The unstructured data submitted by users can contain:
- Invalid characters that break JSON encoding
- Control characters that cause parsing errors
- Unicode edge cases that corrupt transmission
- Whitespace that creates malformed payloads
- Encoding issues that fail UTF-8 validation

**Any of these can cause the API call to fail**, so sanitization is not optional—it's critical for reliability.

---

## What to Sanitize

### 1. **Whitespace Cleanup**

**Problem**: User pastes text with extra spaces, tabs, or irregular formatting

**Solution**: Clean up whitespace intelligently
- Trim leading/trailing whitespace from entire input
- Collapse multiple consecutive spaces to single space
- Collapse tabs and other whitespace to single space
- Preserve intentional line breaks (newlines)

**Example**:
```
Input:  "  Hello    world  \n  Next line  "
Output: "Hello world\nNext line"
```

### 2. **Line Ending Normalization**

**Problem**: Different OS use different line endings (\r\n on Windows, \n on Unix, \r on old Mac)

**Solution**: Normalize all to \n (Unix style)
- Convert \r\n (Windows) → \n
- Convert \r (old Mac) → \n
- Keep \n as-is (Unix/modern)

**Example**:
```
Input:  "Line1\r\nLine2\rLine3\nLine4"
Output: "Line1\nLine2\nLine3\nLine4"
```

### 3. **Control Character Removal**

**Problem**: Copy-pasted text sometimes includes invisible control characters (ASCII 0-31)

**Solution**: Remove dangerous control chars, keep safe ones
- ✓ Keep: \n (newline), \r (carriage return), \t (tab)
- ✗ Remove: \0 (null), \x01-\x08, \x0B, \x0C, \x0E-\x1F, \x7F (delete)

**Example**:
```
Input:  "Text\x00with\x1Fcontrol\nchars"
Output: "Textwithcontrol\nchars"
```

### 4. **Zero-Width Character Removal**

**Problem**: Some text editors and websites embed zero-width characters (invisible, cause parsing issues)

**Solution**: Remove zero-width Unicode characters
- \u200B (zero-width space)
- \u200C (zero-width non-joiner)
- \u200D (zero-width joiner)
- \u200E (left-to-right mark)
- \u200F (right-to-left mark)
- \uFEFF (zero-width no-break space / BOM)

**Example**:
```
Input:  "Zero​width" (has zero-width space between Zero and width)
Output: "Zerowidth"
```

### 5. **Null Byte Removal**

**Problem**: Binary data accidentally pasted includes null bytes that corrupt strings

**Solution**: Strip null bytes (\0)

**Example**:
```
Input:  "Hello\0World"
Output: "HelloWorld"
```

### 6. **UTF-8 Validation**

**Problem**: Malformed UTF-8 sequences cause encoding errors

**Solution**: Validate the final string is valid UTF-8
- Test with TextEncoder (JavaScript)
- Reject if encoding fails
- Return empty string or error on failure

---

## What NOT to Sanitize

### Keep These Characters

✓ **Special characters** - They're valid in unstructured data
- Punctuation: . , ! ? ; : " ' - / \ ( ) [ ] { }
- Symbols: @ # $ % ^ & * + = ~ < >
- Quotes (both single and double)
- Parentheses and brackets

✓ **Emoji** - Preserve them, they're valid Unicode
- "Hello 👋 World" → "Hello 👋 World"

✓ **Unicode characters** - Support international text
- Accents: é, ñ, ü, etc.
- Asian characters: 你好, こんにちは, 안녕하세요
- Right-to-left: العربية, עברית

✓ **Numbers and letters** - Obviously keep these

---

## Implementation Strategy

### Step-by-Step Sanitization

```typescript
function sanitizeRawText(input: string): string {
  // 1. Handle edge cases
  if (!input) return '';

  // 2. Remove null bytes
  input = input.replace(/\0/g, '');

  // 3. Remove control characters (except \t, \n, \r)
  input = input.replace(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/g, '');

  // 4. Remove zero-width characters
  input = input.replace(/[\u200B\u200C\u200D\u200E\u200F\uFEFF]/g, '');

  // 5. Normalize line endings
  input = input.replace(/\r\n/g, '\n').replace(/\r/g, '\n');

  // 6. Clean whitespace per line
  input = input.split('\n').map(line => {
    // Collapse multiple spaces/tabs to single space
    return line.replace(/[ \t]+/g, ' ').trim();
  }).join('\n');

  // 7. Trim entire string
  input = input.trim();

  // 8. Remove excessive blank lines (more than 2 consecutive)
  input = input.replace(/\n\n\n+/g, '\n\n');

  // 9. Validate UTF-8 encoding
  try {
    new TextEncoder().encode(input);
  } catch {
    return ''; // Invalid, reject
  }

  return input;
}
```

### Validation After Sanitization

```typescript
function validateSanitizedInput(input: string): {
  valid: boolean;
  error?: string;
  byteLength?: number;
} {
  // Check not empty
  if (!input || input.length === 0) {
    return {
      valid: false,
      error: 'Text cannot be empty'
    };
  }

  // Check byte length (UTF-8 encoding)
  const byteLength = new TextEncoder().encode(input).length;

  if (byteLength > 100000) {
    return {
      valid: false,
      error: `Text exceeds limit: ${byteLength} bytes (max 100,000)`,
      byteLength
    };
  }

  return { valid: true, byteLength };
}
```

---

## Where to Apply Sanitization

### 1. **On User Input (Real-time)**

```typescript
// PersonForm.tsx
const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
  const raw = e.target.value;
  const sanitized = sanitizeRawText(raw);

  setRawText(sanitized);

  // Validate and show errors
  const validation = validateSanitizedInput(sanitized);
  setCharCount(validation.byteLength || 0);

  if (!validation.valid) {
    setError(validation.error);
  } else {
    setError(null);
  }
};
```

### 2. **Before API Submission**

```typescript
// PersonForm.tsx
const handleSubmit = async () => {
  // Final validation before sending to API
  const validation = validateSanitizedInput(rawText);

  if (!validation.valid) {
    setError(validation.error);
    return;
  }

  // All good - send sanitized text to API
  try {
    await addPersonDataAndRegenerate(
      selectedPersonId,
      rawText,  // Already sanitized
      source
    );
  } catch (err) {
    setError(err.message);
  }
};
```

### 3. **Character Counter**

Display byte count (not character count) since the limit is 100,000 bytes:

```typescript
// Emoji takes 4 bytes in UTF-8
const byteLength = new TextEncoder().encode(sanitized).length;
return <p>Bytes: {byteLength} / 100,000</p>;
```

---

## Service Layer: `sanitizer.ts`

Create a dedicated sanitization service:

```typescript
// src/services/sanitizer.ts

/**
 * Sanitize unstructured text input
 * Removes dangerous characters, normalizes whitespace, validates encoding
 */
export function sanitizeRawText(input: string): string {
  // ... implementation (see above)
}

/**
 * Validate sanitized input against constraints
 */
export function validateSanitizedInput(input: string): {
  valid: boolean;
  error?: string;
  byteLength?: number;
} {
  // ... implementation (see above)
}

/**
 * Escape text for safe JSON transmission
 * (Usually handled by JSON.stringify, but available if needed)
 */
export function escapeForJson(input: string): string {
  return input
    .replace(/\\/g, '\\\\')
    .replace(/"/g, '\\"')
    .replace(/\n/g, '\\n')
    .replace(/\r/g, '\\r')
    .replace(/\t/g, '\\t');
}

/**
 * Get byte length of string (UTF-8 encoded)
 */
export function getByteLength(input: string): number {
  return new TextEncoder().encode(input).length;
}
```

---

## User Feedback

### Display Sanitization Progress

Show the user what's happening:

```
Input Area:
┌─────────────────────────────────────────┐
│ [Textarea with cleaned text]            │
│                                         │
│ Character count: 245 / 100,000 bytes   │
│ ✓ Valid input - ready to submit        │
└─────────────────────────────────────────┘
```

### Error Messages (Clear & Specific)

Display when validation fails:

- ❌ "Text cannot be empty"
- ❌ "Text exceeds 100,000 byte limit (current: 125,000 bytes)"
- ❌ "Invalid UTF-8 encoding detected"
- ❌ "Contains invalid characters - please review"

---

## Testing Scenarios

### ✅ Valid Inputs (Should Pass)

```typescript
// Normal text
"John is a software engineer with 10 years of experience"

// Text with punctuation
"He says: \"Hello, how are you?\" (Excellent!)"

// Text with emoji
"Hello 👋 World 🌍 Nice to meet you!"

// Text with special characters
"Email: john@example.com | Phone: +1 (555) 123-4567"

// International text
"他好 | Bonjour | مرحبا | Привет"

// Multiline text
"Line 1\nLine 2\nLine 3"

// Mixed whitespace (gets normalized)
"Text    with   spaces" → "Text with spaces"
"A\r\nB" → "A\nB"
```

### ❌ Invalid Inputs (Should Be Sanitized)

```typescript
// Extra spaces (collapsed)
"Hello    world" → "Hello world"

// Control characters (removed)
"Text\x00with\x1Fcontrol" → "Textwithcontrol"

// Zero-width characters (removed)
"Zero​width" → "Zerowidth"

// Excessive blank lines (collapsed)
"A\n\n\n\nB" → "A\n\nB"

// Windows line endings (normalized)
"A\r\nB\r\nC" → "A\nB\nC"

// Mixed whitespace (normalized)
"  Text  \t  with  \t  mixed  " → "Text with mixed"
```

### 🚫 Rejected Inputs (Should Show Error)

```typescript
// Empty string
"" → Error: "Text cannot be empty"

// Too long (>100KB)
"x".repeat(100001) → Error: "Exceeds limit: 100,001 bytes"

// Invalid UTF-8
// (TextEncoder will catch and reject)
```

---

## Performance Considerations

- Sanitization is **synchronous** (no async needed)
- Runs on every keystroke (happens instantly)
- Simple regex operations (<1ms per call)
- Can handle 100,000 byte strings efficiently

---

## Security Considerations

⚠️ **This is CLIENT-SIDE sanitization only**

- Use as UX improvement, not security boundary
- API should also validate input
- Don't rely solely on client-side cleaning
- Server-side validation is still required

---

## Checklist for Implementation

- [ ] Create `src/services/sanitizer.ts` with all functions
- [ ] Import in PersonForm component
- [ ] Add sanitization to `handleInputChange`
- [ ] Add validation to `handleSubmit`
- [ ] Display byte counter (not character count)
- [ ] Show clear error messages
- [ ] Test with special characters
- [ ] Test with emoji
- [ ] Test with very long text
- [ ] Test with control characters
- [ ] Verify API receives clean data

---

## Related Files

- `PLAN.md` - Full specification (section: PersonForm Validation & Sanitization)
- `PersonForm.tsx` - Component using sanitization
- `src/services/sanitizer.ts` - Implementation (to be created)

---

**Status**: Specification Complete - Ready for Implementation
