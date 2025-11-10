/**
 * PersonaDisplay Component
 *
 * Displays the generated persona with metadata and formatted JSON.
 * Includes copy to clipboard functionality.
 */

'use client';

import { useState } from 'react';
import type { Persona } from '@/services/types';

interface PersonaDisplayProps {
  persona: Persona | null;
  personDataCount: number;
  isLoading: boolean;
  onRefresh?: () => Promise<void>;
}

export default function PersonaDisplay({
  persona,
  personDataCount,
  isLoading,
  onRefresh,
}: PersonaDisplayProps) {
  const [isCopied, setIsCopied] = useState(false);

  const handleCopyJson = async () => {
    if (!persona) return;

    try {
      const jsonString = JSON.stringify(persona.persona, null, 2);
      await navigator.clipboard.writeText(jsonString);
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy JSON:', err);
    }
  };

  const handleRefresh = async () => {
    if (onRefresh) {
      try {
        await onRefresh();
      } catch (err) {
        console.error('Failed to refresh persona:', err);
      }
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  };

  return (
    <div className="bg-white border border-gray-300 rounded-lg p-6 shadow-sm">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-gray-800">Generated Persona</h2>
        <div className="flex gap-2">
          {onRefresh && (
            <button
              onClick={handleRefresh}
              disabled={isLoading || !persona}
              className="px-3 py-1 text-sm bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
            >
              Refresh
            </button>
          )}
          <button
            onClick={handleCopyJson}
            disabled={!persona}
            className="px-3 py-1 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            {isCopied ? 'Copied!' : 'Copy JSON'}
          </button>
        </div>
      </div>

      {isLoading ? (
        <div className="flex justify-center items-center h-48">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-3 text-gray-600">Loading persona...</span>
        </div>
      ) : persona ? (
        <>
          {/* Metadata */}
          <div className="mb-4 p-3 bg-gray-50 border border-gray-200 rounded-md">
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span className="font-semibold text-gray-700">Persona ID:</span>
                <span className="ml-2 text-gray-600">{persona.id}</span>
              </div>
              <div>
                <span className="font-semibold text-gray-700">Version:</span>
                <span className="ml-2 text-gray-600">{persona.version}</span>
              </div>
              <div>
                <span className="font-semibold text-gray-700">Created:</span>
                <span className="ml-2 text-gray-600">{formatDate(persona.created_at)}</span>
              </div>
              <div>
                <span className="font-semibold text-gray-700">Data Count:</span>
                <span className="ml-2 text-gray-600">{personDataCount}</span>
              </div>
              <div className="col-span-2">
                <span className="font-semibold text-gray-700">Computed From:</span>
                <span className="ml-2 text-gray-600">{persona.computed_from_data_ids.length} data points</span>
              </div>
            </div>
          </div>

          {/* JSON Display */}
          <div className="bg-gray-900 text-gray-100 p-4 rounded-md overflow-auto max-h-96">
            <pre className="text-sm font-mono whitespace-pre-wrap">
              {JSON.stringify(persona.persona, null, 2)}
            </pre>
          </div>
        </>
      ) : (
        <div className="flex justify-center items-center h-48 text-gray-500">
          <p>No persona generated yet. Submit data to create a persona.</p>
        </div>
      )}
    </div>
  );
}
