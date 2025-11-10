/**
 * Input Sanitization & Validation Service
 *
 * Cleans and validates unstructured text input for the Person Aggregate Root API.
 * Removes dangerous characters, normalizes whitespace, and validates encoding.
 */

/**
 * Sanitize unstructured text input
 * Removes dangerous characters, normalizes whitespace, validates encoding
 *
 * @param input - Raw text input from user
 * @returns Sanitized text ready for API submission
 */
export function sanitizeRawText(input: string): string {
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

/**
 * Validate sanitized input against API constraints
 *
 * @param input - Sanitized text to validate
 * @returns Validation result with error message if invalid
 */
export function validateSanitizedInput(input: string): {
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
      error: `Text exceeds limit: ${byteLength.toLocaleString()} bytes (max 100,000)`,
      byteLength
    };
  }

  return { valid: true, byteLength };
}

/**
 * Escape text for safe JSON transmission
 * (Usually handled by JSON.stringify, but available if needed)
 *
 * @param input - Text to escape
 * @returns Escaped text
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
 *
 * @param input - Text to measure
 * @returns Byte length
 */
export function getByteLength(input: string): number {
  return new TextEncoder().encode(input).length;
}
