/**
 * Main Page - Person Aggregate Root API Test App
 *
 * Orchestrates all components and manages global state.
 * Tests two user flows:
 * 1. Create new person with persona
 * 2. Update existing person with new data
 */

'use client';

import { useState, useCallback, useEffect } from 'react';
import PersonSelector from '@/components/PersonSelector';
import PersonForm from '@/components/PersonForm';
import PersonaDisplay from '@/components/PersonaDisplay';
import ApiDebugPanel from '@/components/ApiDebugPanel';
import { usePersons } from '@/hooks/usePersons';
import { addPersonDataAndRegenerate, getPersona, getApiCalls, clearApiCalls } from '@/services/api';
import type { Persona, DataSource } from '@/services/types';

export default function Home() {
  // State management
  const [selectedPersonId, setSelectedPersonId] = useState<string | null>(null);
  const [currentPersona, setCurrentPersona] = useState<Persona | null>(null);
  const [isLoadingPersona, setIsLoadingPersona] = useState<boolean>(false);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [isDebugOpen, setIsDebugOpen] = useState<boolean>(true);

  // Custom hook for persons management
  const { persons, isLoading, error: personsError, refreshPersons, addNewPerson } = usePersons();

  // Get current person data count
  const currentPersonDataCount = persons.find(p => p.id === selectedPersonId)?.person_data_count || 0;

  /**
   * Handle person selection
   */
  const handlePersonSelect = useCallback(async (personId: string | null) => {
    setSelectedPersonId(personId);
    setCurrentPersona(null);
    setError(null);

    if (personId) {
      // Load persona for selected person (if exists)
      const person = persons.find(p => p.id === personId);
      if (person && person.latest_persona_version !== null) {
        setIsLoadingPersona(true);
        try {
          const persona = await getPersona(personId);
          setCurrentPersona(persona);
        } catch (err) {
          console.error('Failed to load persona:', err);
          // Not a critical error - user can still submit data
        } finally {
          setIsLoadingPersona(false);
        }
      }
    }
  }, [persons]);

  /**
   * Handle creating new person
   */
  const handleCreateNewPerson = useCallback(async () => {
    setError(null);
    try {
      const newPerson = await addNewPerson();
      setSelectedPersonId(newPerson.id);
      setCurrentPersona(null);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to create person';
      setError(errorMessage);
    }
  }, [addNewPerson]);

  /**
   * Handle data submission
   */
  const handleDataSubmit = useCallback(async (rawText: string, source: DataSource) => {
    if (!selectedPersonId) {
      setError('No person selected');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const result = await addPersonDataAndRegenerate(selectedPersonId, rawText, source);
      setCurrentPersona(result.persona);
      await refreshPersons();
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to submit data';
      setError(errorMessage);
      throw err;
    } finally {
      setIsSubmitting(false);
    }
  }, [selectedPersonId, refreshPersons]);

  /**
   * Handle persona refresh
   */
  const handleRefreshPersona = useCallback(async () => {
    if (!selectedPersonId) return;

    setIsLoadingPersona(true);
    setError(null);

    try {
      const persona = await getPersona(selectedPersonId);
      setCurrentPersona(persona);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to refresh persona';
      setError(errorMessage);
    } finally {
      setIsLoadingPersona(false);
    }
  }, [selectedPersonId]);

  /**
   * Auto-select first person if none selected
   */
  useEffect(() => {
    if (!selectedPersonId && persons.length > 0) {
      handlePersonSelect(persons[0].id);
    }
  }, [persons, selectedPersonId, handlePersonSelect]);

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-blue-600 text-white p-6 shadow-lg">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold">Person Aggregate Root API - Test App</h1>
          <p className="mt-2 text-blue-100">
            Test and verify API endpoints with real-time debugging
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto p-6">
        {/* Error Display */}
        {(error || personsError) && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-800 font-semibold">Error:</p>
            <p className="text-red-700">{error || personsError}</p>
          </div>
        )}

        {/* Layout Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Column */}
          <div className="space-y-6">
            {/* Person Selector */}
            <PersonSelector
              persons={persons}
              selectedPersonId={selectedPersonId}
              onSelect={handlePersonSelect}
              onCreateNew={handleCreateNewPerson}
              isLoading={isLoading}
            />

            {/* Person Form */}
            <PersonForm
              personId={selectedPersonId}
              isLoading={isSubmitting}
              onSubmit={handleDataSubmit}
            />
          </div>

          {/* Right Column */}
          <div className="space-y-6">
            {/* Persona Display */}
            <PersonaDisplay
              persona={currentPersona}
              personDataCount={currentPersonDataCount}
              isLoading={isLoadingPersona}
              onRefresh={handleRefreshPersona}
            />
          </div>
        </div>

        {/* Debug Panel */}
        <div className="mt-6">
          <ApiDebugPanel
            calls={getApiCalls()}
            isOpen={isDebugOpen}
            onToggle={() => setIsDebugOpen(!isDebugOpen)}
            onClear={clearApiCalls}
          />
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-gray-300 p-6 mt-12">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-sm">
            Person Aggregate Root API Test Application | Built with Next.js 16 + TypeScript
          </p>
        </div>
      </footer>
    </div>
  );
}
