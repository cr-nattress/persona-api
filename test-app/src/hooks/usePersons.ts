/**
 * Custom Hook for Person Management
 *
 * Manages person list state and provides methods for creating and refreshing persons.
 */

import { useState, useEffect, useCallback } from 'react';
import { createPerson, listPersons } from '@/services/api';
import type { Person } from '@/services/types';

export function usePersons() {
  const [persons, setPersons] = useState<Person[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Refresh the persons list from the API
   */
  const refreshPersons = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await listPersons(100, 0);
      setPersons(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch persons';
      setError(errorMessage);
      console.error('Error fetching persons:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Create a new person with optional demographic information and refresh the list
   */
  const addNewPerson = useCallback(async (
    firstName?: string,
    lastName?: string,
    gender?: string
  ): Promise<Person> => {
    setIsLoading(true);
    setError(null);

    try {
      const newPerson = await createPerson(firstName, lastName, gender);
      await refreshPersons();
      return newPerson;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to create person';
      setError(errorMessage);
      console.error('Error creating person:', err);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [refreshPersons]);

  /**
   * Load persons on mount
   */
  useEffect(() => {
    refreshPersons();
  }, [refreshPersons]);

  return {
    persons,
    isLoading,
    error,
    refreshPersons,
    addNewPerson,
  };
}
