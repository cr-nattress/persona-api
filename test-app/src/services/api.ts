/**
 * API Client for Person Aggregate Root API
 *
 * Provides typed functions for all API endpoints with logging for debug panel.
 */

import type {
  Person,
  PersonData,
  Persona,
  AddDataAndRegenerateResponse,
  PersonDataHistoryResponse,
  ApiCall,
  DataSource,
} from './types';

// API Base URL from environment
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8080';

// API Call logging registry
const apiCallLog: ApiCall[] = [];

/**
 * Generate unique ID for API call
 */
function generateCallId(): string {
  return `call-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Log an API call for the debug panel
 */
function logApiCall(call: Omit<ApiCall, 'id' | 'timestamp'>): void {
  const logEntry: ApiCall = {
    id: generateCallId(),
    timestamp: new Date().toISOString(),
    ...call,
  };
  apiCallLog.push(logEntry);
  console.log('[API Call]', logEntry);
}

/**
 * Get all logged API calls
 */
export function getApiCalls(): ApiCall[] {
  return [...apiCallLog];
}

/**
 * Clear API call log
 */
export function clearApiCalls(): void {
  apiCallLog.length = 0;
}

/**
 * Handle API errors
 */
function handleApiError(error: unknown, endpoint: string): never {
  if (error instanceof Error) {
    throw new Error(`API Error (${endpoint}): ${error.message}`);
  }
  throw new Error(`API Error (${endpoint}): Unknown error`);
}

/**
 * Create a new person with optional demographic information
 *
 * @param firstName - Optional first name of the person
 * @param lastName - Optional last name of the person
 * @param gender - Optional gender of the person
 * @returns The newly created person
 */
export async function createPerson(
  firstName?: string,
  lastName?: string,
  gender?: string
): Promise<Person> {
  const endpoint = `${API_BASE_URL}/v1/person`;
  const startTime = Date.now();

  const requestBody: Record<string, string | null> = {};
  if (firstName) requestBody.first_name = firstName;
  if (lastName) requestBody.last_name = lastName;
  if (gender) requestBody.gender = gender;

  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    });

    const duration = Date.now() - startTime;
    const data = await response.json();

    logApiCall({
      method: 'POST',
      endpoint: '/v1/person',
      status: response.status,
      duration,
      request: requestBody,
      response: data,
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${JSON.stringify(data)}`);
    }

    return data as Person;
  } catch (error) {
    const duration = Date.now() - startTime;
    logApiCall({
      method: 'POST',
      endpoint: '/v1/person',
      status: 0,
      duration,
      request: requestBody,
      error: error instanceof Error ? error.message : 'Unknown error',
    });
    handleApiError(error, endpoint);
  }
}

/**
 * List all persons
 *
 * @param limit - Maximum number of persons to return (default 100)
 * @param offset - Number of persons to skip (default 0)
 * @returns Array of persons
 */
export async function listPersons(limit: number = 100, offset: number = 0): Promise<Person[]> {
  const endpoint = `${API_BASE_URL}/v1/person?limit=${limit}&offset=${offset}`;
  const startTime = Date.now();

  try {
    const response = await fetch(endpoint, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const duration = Date.now() - startTime;
    const data = await response.json();

    logApiCall({
      method: 'GET',
      endpoint: `/v1/person?limit=${limit}&offset=${offset}`,
      status: response.status,
      duration,
      response: data,
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${JSON.stringify(data)}`);
    }

    return data as Person[];
  } catch (error) {
    const duration = Date.now() - startTime;
    logApiCall({
      method: 'GET',
      endpoint: `/v1/person?limit=${limit}&offset=${offset}`,
      status: 0,
      duration,
      error: error instanceof Error ? error.message : 'Unknown error',
    });
    handleApiError(error, endpoint);
  }
}

/**
 * Add person data and regenerate persona
 *
 * @param personId - ID of the person
 * @param rawText - Unstructured text data (must be sanitized)
 * @param source - Source of the data
 * @returns The created person data and regenerated persona
 */
export async function addPersonDataAndRegenerate(
  personId: string,
  rawText: string,
  source: DataSource
): Promise<AddDataAndRegenerateResponse> {
  // Build query parameters
  const queryParams = new URLSearchParams({
    raw_text: rawText,
    source: source,
  });

  const endpoint = `${API_BASE_URL}/v1/person/${personId}/data-and-regenerate?${queryParams.toString()}`;
  const startTime = Date.now();

  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const duration = Date.now() - startTime;
    const data = await response.json();

    logApiCall({
      method: 'POST',
      endpoint: `/v1/person/${personId}/data-and-regenerate?raw_text=...&source=${source}`,
      status: response.status,
      duration,
      response: data,
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${JSON.stringify(data)}`);
    }

    return data as AddDataAndRegenerateResponse;
  } catch (error) {
    const duration = Date.now() - startTime;
    logApiCall({
      method: 'POST',
      endpoint: `/v1/person/${personId}/data-and-regenerate?raw_text=...&source=${source}`,
      status: 0,
      duration,
      error: error instanceof Error ? error.message : 'Unknown error',
    });
    handleApiError(error, endpoint);
  }
}

/**
 * Get the latest persona for a person
 *
 * @param personId - ID of the person
 * @returns The latest persona
 */
export async function getPersona(personId: string): Promise<Persona> {
  const endpoint = `${API_BASE_URL}/v1/person/${personId}/persona`;
  const startTime = Date.now();

  try {
    const response = await fetch(endpoint, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const duration = Date.now() - startTime;
    const data = await response.json();

    logApiCall({
      method: 'GET',
      endpoint: `/v1/person/${personId}/persona`,
      status: response.status,
      duration,
      response: data,
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${JSON.stringify(data)}`);
    }

    return data as Persona;
  } catch (error) {
    const duration = Date.now() - startTime;
    logApiCall({
      method: 'GET',
      endpoint: `/v1/person/${personId}/persona`,
      status: 0,
      duration,
      error: error instanceof Error ? error.message : 'Unknown error',
    });
    handleApiError(error, endpoint);
  }
}

/**
 * Get person data history
 *
 * @param personId - ID of the person
 * @param limit - Maximum number of items to return (default 10)
 * @param offset - Number of items to skip (default 0)
 * @returns Person data history with pagination info
 */
export async function getPersonDataHistory(
  personId: string,
  limit: number = 10,
  offset: number = 0
): Promise<PersonDataHistoryResponse> {
  const endpoint = `${API_BASE_URL}/v1/person/${personId}/data?limit=${limit}&offset=${offset}`;
  const startTime = Date.now();

  try {
    const response = await fetch(endpoint, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const duration = Date.now() - startTime;
    const data = await response.json();

    logApiCall({
      method: 'GET',
      endpoint: `/v1/person/${personId}/data?limit=${limit}&offset=${offset}`,
      status: response.status,
      duration,
      response: data,
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${JSON.stringify(data)}`);
    }

    return data as PersonDataHistoryResponse;
  } catch (error) {
    const duration = Date.now() - startTime;
    logApiCall({
      method: 'GET',
      endpoint: `/v1/person/${personId}/data?limit=${limit}&offset=${offset}`,
      status: 0,
      duration,
      error: error instanceof Error ? error.message : 'Unknown error',
    });
    handleApiError(error, endpoint);
  }
}
