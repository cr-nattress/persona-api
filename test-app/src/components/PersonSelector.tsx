/**
 * PersonSelector Component
 *
 * Dropdown for selecting a person or creating a new one.
 * Shows person IDs, creation dates, and data counts.
 * Includes optional demographic form fields for person creation.
 */

'use client';

import { useState } from 'react';
import type { Person } from '@/services/types';

interface PersonSelectorProps {
  persons: Person[];
  selectedPersonId: string | null;
  onSelect: (personId: string | null) => void;
  onCreateNew: (firstName?: string, lastName?: string, gender?: string) => Promise<void>;
  isLoading: boolean;
}

export default function PersonSelector({
  persons,
  selectedPersonId,
  onSelect,
  onCreateNew,
  isLoading,
}: PersonSelectorProps) {
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [gender, setGender] = useState('');

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
      await onCreateNew(
        firstName || undefined,
        lastName || undefined,
        gender || undefined
      );
      // Reset form on success
      setFirstName('');
      setLastName('');
      setGender('');
      setShowCreateForm(false);
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
                {person.first_name && person.last_name
                  ? `${person.first_name} ${person.last_name}`
                  : person.id.substring(0, 8)}... | Created: {formatDate(person.created_at)} | Data: {person.person_data_count}
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
            onClick={() => setShowCreateForm(!showCreateForm)}
            disabled={isLoading}
            className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:bg-gray-300 disabled:cursor-not-allowed font-medium whitespace-nowrap"
          >
            {showCreateForm ? 'Cancel' : '+ Create New'}
          </button>
        </div>
      </div>

      {/* Create Person Form */}
      {showCreateForm && (
        <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-md">
          <p className="text-sm font-semibold text-gray-800 mb-3">Create New Person (Optional Fields)</p>
          <div className="grid grid-cols-3 gap-3">
            <div>
              <label htmlFor="firstName" className="block text-xs font-medium text-gray-700 mb-1">
                First Name
              </label>
              <input
                id="firstName"
                type="text"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                placeholder="John"
                disabled={isLoading}
                className="w-full px-2 py-1 border border-gray-300 rounded text-sm focus:outline-none focus:ring-2 focus:ring-green-500 disabled:bg-gray-100"
              />
            </div>
            <div>
              <label htmlFor="lastName" className="block text-xs font-medium text-gray-700 mb-1">
                Last Name
              </label>
              <input
                id="lastName"
                type="text"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                placeholder="Doe"
                disabled={isLoading}
                className="w-full px-2 py-1 border border-gray-300 rounded text-sm focus:outline-none focus:ring-2 focus:ring-green-500 disabled:bg-gray-100"
              />
            </div>
            <div>
              <label htmlFor="gender" className="block text-xs font-medium text-gray-700 mb-1">
                Gender
              </label>
              <select
                id="gender"
                value={gender}
                onChange={(e) => setGender(e.target.value)}
                disabled={isLoading}
                className="w-full px-2 py-1 border border-gray-300 rounded text-sm focus:outline-none focus:ring-2 focus:ring-green-500 disabled:bg-gray-100"
              >
                <option value="">--</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
                <option value="prefer not to say">Prefer not to say</option>
              </select>
            </div>
          </div>
          <button
            type="button"
            onClick={handleCreateNew}
            disabled={isLoading}
            className="mt-3 w-full px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:bg-gray-300 disabled:cursor-not-allowed font-medium"
          >
            {isLoading ? 'Creating...' : 'Create Person'}
          </button>
        </div>
      )}

      {/* Selected Person Info */}
      {selectedPersonId && (
        <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-md">
          <p className="text-sm text-gray-700">
            <span className="font-semibold">Selected Person ID:</span> {selectedPersonId}
          </p>
          {persons.find(p => p.id === selectedPersonId) && (
            <>
              {persons.find(p => p.id === selectedPersonId)?.first_name && (
                <p className="text-sm text-gray-700 mt-1">
                  <span className="font-semibold">Name:</span> {persons.find(p => p.id === selectedPersonId)?.first_name} {persons.find(p => p.id === selectedPersonId)?.last_name}
                </p>
              )}
              {persons.find(p => p.id === selectedPersonId)?.gender && (
                <p className="text-sm text-gray-700 mt-1">
                  <span className="font-semibold">Gender:</span> {persons.find(p => p.id === selectedPersonId)?.gender}
                </p>
              )}
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
