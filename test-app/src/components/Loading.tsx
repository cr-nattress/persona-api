/**
 * Loading Component
 *
 * Simple loading indicator with optional message.
 */

'use client';

interface LoadingProps {
  isLoading: boolean;
  message?: string;
}

export default function Loading({ isLoading, message = 'Loading...' }: LoadingProps) {
  if (!isLoading) return null;

  return (
    <div className="flex justify-center items-center p-8">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      <span className="ml-3 text-gray-600">{message}</span>
    </div>
  );
}
