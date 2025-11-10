/**
 * TypeScript Type Definitions for Person Aggregate Root API
 */

/**
 * Person entity - the aggregate root
 */
export interface Person {
  id: string;
  created_at: string;
  updated_at: string;
  person_data_count: number;
  latest_persona_version: number | null;
}

/**
 * PersonData entity - unstructured data submitted about a person
 */
export interface PersonData {
  id: string;
  person_id: string;
  raw_text: string;
  source: string;
  created_at: string;
}

/**
 * Persona entity - AI-generated structured profile
 */
export interface Persona {
  id: string;
  person_id: string;
  persona: Record<string, unknown>;
  version: number;
  computed_from_data_ids: string[];
  created_at: string;
}

/**
 * Response from adding data and regenerating persona
 */
export interface AddDataAndRegenerateResponse {
  person_data: PersonData;
  persona: Persona;
}

/**
 * Response from getting person data history
 */
export interface PersonDataHistoryResponse {
  items: PersonData[];
  total: number;
  limit: number;
  offset: number;
}

/**
 * API Call log entry for debug panel
 */
export interface ApiCall {
  id: string;
  timestamp: string;
  method: string;
  endpoint: string;
  status: number;
  duration: number;
  request?: unknown;
  response?: unknown;
  error?: string;
}

/**
 * Data source options for person data
 */
export type DataSource = 'api' | 'web' | 'email' | 'chat' | 'interview' | 'document' | 'other';
