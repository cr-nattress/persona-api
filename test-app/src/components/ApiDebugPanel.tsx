/**
 * ApiDebugPanel Component
 *
 * Collapsible debug panel showing all API calls with request/response details.
 * Useful for troubleshooting and understanding API interactions.
 */

'use client';

import { useState } from 'react';
import type { ApiCall } from '@/services/types';

interface ApiDebugPanelProps {
  calls: ApiCall[];
  isOpen: boolean;
  onToggle: () => void;
  onClear: () => void;
}

export default function ApiDebugPanel({
  calls,
  isOpen,
  onToggle,
  onClear,
}: ApiDebugPanelProps) {
  const [expandedCallId, setExpandedCallId] = useState<string | null>(null);

  const handleCopyAll = async () => {
    try {
      const jsonString = JSON.stringify(calls, null, 2);
      await navigator.clipboard.writeText(jsonString);
    } catch (err) {
      console.error('Failed to copy API calls:', err);
    }
  };

  const handleCopyCall = async (call: ApiCall) => {
    try {
      const jsonString = JSON.stringify(call, null, 2);
      await navigator.clipboard.writeText(jsonString);
    } catch (err) {
      console.error('Failed to copy API call:', err);
    }
  };

  const toggleExpand = (callId: string) => {
    setExpandedCallId(expandedCallId === callId ? null : callId);
  };

  const getStatusColor = (status: number) => {
    if (status === 0) return 'text-red-600';
    if (status >= 200 && status < 300) return 'text-green-600';
    if (status >= 400 && status < 500) return 'text-yellow-600';
    if (status >= 500) return 'text-red-600';
    return 'text-gray-600';
  };

  const getStatusBgColor = (status: number) => {
    if (status === 0) return 'bg-red-50 border-red-200';
    if (status >= 200 && status < 300) return 'bg-green-50 border-green-200';
    if (status >= 400 && status < 500) return 'bg-yellow-50 border-yellow-200';
    if (status >= 500) return 'bg-red-50 border-red-200';
    return 'bg-gray-50 border-gray-200';
  };

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString();
  };

  return (
    <div className="bg-white border border-gray-300 rounded-lg shadow-sm">
      {/* Header */}
      <div
        className="flex justify-between items-center p-4 cursor-pointer hover:bg-gray-50"
        onClick={onToggle}
      >
        <div className="flex items-center gap-2">
          <h2 className="text-xl font-semibold text-gray-800">Debug Panel</h2>
          <span className="px-2 py-1 text-xs bg-gray-200 text-gray-700 rounded-full">
            {calls.length} {calls.length === 1 ? 'call' : 'calls'}
          </span>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={(e) => {
              e.stopPropagation();
              handleCopyAll();
            }}
            disabled={calls.length === 0}
            className="px-3 py-1 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            Copy All
          </button>
          <button
            onClick={(e) => {
              e.stopPropagation();
              onClear();
            }}
            disabled={calls.length === 0}
            className="px-3 py-1 text-sm bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            Clear
          </button>
          <span className="text-gray-500">
            {isOpen ? '▼' : '▶'}
          </span>
        </div>
      </div>

      {/* Content */}
      {isOpen && (
        <div className="border-t border-gray-300 p-4 max-h-96 overflow-y-auto bg-gray-50">
          {calls.length === 0 ? (
            <p className="text-center text-gray-500 py-8">No API calls yet</p>
          ) : (
            <div className="space-y-2">
              {calls.map((call) => (
                <div
                  key={call.id}
                  className={`border rounded-md ${getStatusBgColor(call.status)}`}
                >
                  {/* Call Summary */}
                  <div
                    className="flex justify-between items-center p-3 cursor-pointer hover:bg-white/50"
                    onClick={() => toggleExpand(call.id)}
                  >
                    <div className="flex items-center gap-3 flex-1">
                      <span className="font-mono text-xs font-semibold px-2 py-1 bg-white rounded">
                        {call.method}
                      </span>
                      <span className="text-sm font-mono text-gray-700 truncate">
                        {call.endpoint}
                      </span>
                      <span className={`text-sm font-semibold ${getStatusColor(call.status)}`}>
                        {call.status === 0 ? 'ERROR' : call.status}
                      </span>
                      <span className="text-xs text-gray-500">{call.duration}ms</span>
                      <span className="text-xs text-gray-500">{formatTimestamp(call.timestamp)}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleCopyCall(call);
                        }}
                        className="px-2 py-1 text-xs bg-white text-gray-700 rounded hover:bg-gray-100"
                      >
                        Copy
                      </button>
                      <span className="text-gray-500 text-xs">
                        {expandedCallId === call.id ? '▼' : '▶'}
                      </span>
                    </div>
                  </div>

                  {/* Expanded Details */}
                  {expandedCallId === call.id && (
                    <div className="border-t border-gray-300 p-3 bg-white">
                      {/* Request */}
                      {!!call.request && (
                        <div className="mb-3">
                          <h4 className="text-xs font-semibold text-gray-700 mb-1">Request:</h4>
                          <pre className="text-xs font-mono bg-gray-900 text-gray-100 p-2 rounded overflow-x-auto">
                            {JSON.stringify(call.request, null, 2)}
                          </pre>
                        </div>
                      )}

                      {/* Response */}
                      {!!call.response && (
                        <div className="mb-3">
                          <h4 className="text-xs font-semibold text-gray-700 mb-1">Response:</h4>
                          <pre className="text-xs font-mono bg-gray-900 text-gray-100 p-2 rounded overflow-x-auto max-h-48">
                            {JSON.stringify(call.response, null, 2)}
                          </pre>
                        </div>
                      )}

                      {/* Error */}
                      {call.error && (
                        <div>
                          <h4 className="text-xs font-semibold text-red-700 mb-1">Error:</h4>
                          <pre className="text-xs font-mono bg-red-900 text-red-100 p-2 rounded overflow-x-auto">
                            {call.error}
                          </pre>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
