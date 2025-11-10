/**
 * PersonForm Component
 *
 * Form for submitting unstructured data about a person.
 * Includes real-time input sanitization, validation, and byte counter.
 */

'use client';

import { useState, useEffect } from 'react';
import { sanitizeRawText, validateSanitizedInput, getByteLength } from '@/services/sanitizer';
import type { DataSource } from '@/services/types';

interface PersonFormProps {
  personId: string | null;
  isLoading: boolean;
  onSubmit: (rawText: string, source: DataSource) => Promise<void>;
}

const DATA_SOURCES: { value: DataSource; label: string }[] = [
  { value: 'api', label: 'API' },
  { value: 'web', label: 'Web' },
  { value: 'email', label: 'Email' },
  { value: 'chat', label: 'Chat' },
  { value: 'interview', label: 'Interview' },
  { value: 'document', label: 'Document' },
  { value: 'other', label: 'Other' },
];

export default function PersonForm({ personId, isLoading, onSubmit }: PersonFormProps) {
  const [rawText, setRawText] = useState<string>('');
  const [source, setSource] = useState<DataSource>('api');
  const [error, setError] = useState<string | null>(null);
  const [byteCount, setByteCount] = useState<number>(0);

  // Reset form when person changes
  useEffect(() => {
    setRawText('');
    setError(null);
    setByteCount(0);
  }, [personId]);

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const raw = e.target.value;
    const sanitized = sanitizeRawText(raw);

    setRawText(sanitized);

    // Validate and show errors
    const validation = validateSanitizedInput(sanitized);
    setByteCount(validation.byteLength || 0);

    if (!validation.valid && sanitized.length > 0) {
      setError(validation.error || null);
    } else {
      setError(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Check if person is selected
    if (!personId) {
      setError('Please select or create a person first');
      return;
    }

    // Final validation before sending to API
    const validation = validateSanitizedInput(rawText);

    if (!validation.valid) {
      setError(validation.error || 'Invalid input');
      return;
    }

    setError(null);

    try {
      await onSubmit(rawText, source);
      // Clear form on success
      setRawText('');
      setByteCount(0);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to submit data';
      setError(errorMessage);
    }
  };

  const handleClear = () => {
    setRawText('');
    setError(null);
    setByteCount(0);
  };

  const isSubmitDisabled = !personId || isLoading || rawText.trim().length === 0 || !!error;

  return (
    <div className="bg-white border border-gray-300 rounded-lg p-6 shadow-sm">
      <h2 className="text-xl font-semibold mb-4 text-gray-800">Data Submission</h2>

      <form onSubmit={handleSubmit}>
        {/* Textarea */}
        <div className="mb-4">
          <label htmlFor="rawText" className="block text-sm font-medium text-gray-700 mb-2">
            Unstructured Text Data
          </label>
          <textarea
            id="rawText"
            value={rawText}
            onChange={handleInputChange}
            disabled={isLoading}
            placeholder="Enter unstructured data about the person..."
            className="w-full h-48 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-y font-mono text-sm disabled:bg-gray-100 disabled:cursor-not-allowed"
            rows={10}
          />
          <div className="mt-2 flex justify-between items-center">
            <span className={`text-sm ${byteCount > 100000 ? 'text-red-600 font-semibold' : 'text-gray-600'}`}>
              Bytes: {byteCount.toLocaleString()} / 100,000
            </span>
            {error && (
              <span className="text-sm text-red-600">{error}</span>
            )}
            {!error && rawText.length > 0 && (
              <span className="text-sm text-green-600">Valid input</span>
            )}
          </div>
        </div>

        {/* Source Selection */}
        <div className="mb-4">
          <label htmlFor="source" className="block text-sm font-medium text-gray-700 mb-2">
            Data Source
          </label>
          <select
            id="source"
            value={source}
            onChange={(e) => setSource(e.target.value as DataSource)}
            disabled={isLoading}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
          >
            {DATA_SOURCES.map((src) => (
              <option key={src.value} value={src.value}>
                {src.label}
              </option>
            ))}
          </select>
        </div>

        {/* Buttons */}
        <div className="flex gap-3">
          <button
            type="submit"
            disabled={isSubmitDisabled}
            className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-gray-300 disabled:cursor-not-allowed disabled:text-gray-500 font-medium"
          >
            {isLoading ? 'Submitting...' : 'Submit Data'}
          </button>
          <button
            type="button"
            onClick={handleClear}
            disabled={isLoading}
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 disabled:bg-gray-100 disabled:cursor-not-allowed font-medium"
          >
            Clear
          </button>
        </div>
      </form>
    </div>
  );
}
