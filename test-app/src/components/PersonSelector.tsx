/**
 * PersonSelector Component
 *
 * Dropdown for selecting a person or creating a new one.
 * Shows person IDs, creation dates, and data counts.
 */

'use client';

import type { Person } from '@/services/types';

interface PersonSelectorProps {
  persons: Person[];
  selectedPersonId: string | null;
  onSelect: (personId: string | null) => void;
  onCreateNew: () => Promise<void>;
  isLoading: boolean;
}

export default function PersonSelector({
  persons,
  selectedPersonId,
  onSelect,
  onCreateNew,
  isLoading,
}: PersonSelectorProps) {
  const handleSelectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    if (value === '') {
      onSelect(null);
    } else {
      onSelect(value);
    }
  };

  const handleCreateNew = async () => {
    try {
      await onCreateNew();
    } catch (err) {
      console.error('Failed to create new person:', err);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  };

  return (
    <div className="bg-white border border-gray-300 rounded-lg p-6 shadow-sm">
      <h2 className="text-xl font-semibold mb-4 text-gray-800">Person Management</h2>

      <div className="flex gap-3">
        {/* Dropdown */}
        <div className="flex-1">
          <label htmlFor="personSelect" className="block text-sm font-medium text-gray-700 mb-2">
            Select Person
          </label>
          <select
            id="personSelect"
            value={selectedPersonId || ''}
            onChange={handleSelectChange}
            disabled={isLoading}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
          >
            <option value="">-- Choose a person --</option>
            {persons.map((person) => (
              <option key={person.id} value={person.id}>
                {person.id.substring(0, 8)}... | Created: {formatDate(person.created_at)} | Data: {person.person_data_count} | Version: {person.latest_persona_version || 'N/A'}
              </option>
            ))}
          </select>
          {persons.length === 0 && !isLoading && (
            <p className="mt-2 text-sm text-gray-500">No persons found. Create one to get started.</p>
          )}
        </div>

        {/* Create New Button */}
        <div className="flex items-end">
          <button
            type="button"
            onClick={handleCreateNew}
            disabled={isLoading}
            className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:bg-gray-300 disabled:cursor-not-allowed font-medium whitespace-nowrap"
          >
            {isLoading ? 'Creating...' : '+ Create New'}
          </button>
        </div>
      </div>

      {/* Selected Person Info */}
      {selectedPersonId && (
        <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-md">
          <p className="text-sm text-gray-700">
            <span className="font-semibold">Selected Person ID:</span> {selectedPersonId}
          </p>
          {persons.find(p => p.id === selectedPersonId) && (
            <>
              <p className="text-sm text-gray-700 mt-1">
                <span className="font-semibold">Data Count:</span> {persons.find(p => p.id === selectedPersonId)?.person_data_count}
              </p>
              <p className="text-sm text-gray-700 mt-1">
                <span className="font-semibold">Latest Persona Version:</span> {persons.find(p => p.id === selectedPersonId)?.latest_persona_version || 'None'}
              </p>
            </>
          )}
        </div>
      )}
    </div>
  );
}
