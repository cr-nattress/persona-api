-- Migration: Create personas table
-- Description: Initial schema for storing persona data
-- Date: 2025-11-06

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create personas table
CREATE TABLE IF NOT EXISTS public.personas (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  raw_text TEXT NOT NULL,
  persona JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create index on created_at for sorting/filtering
CREATE INDEX IF NOT EXISTS idx_personas_created_at ON public.personas(created_at DESC);

-- Create index on updated_at for sorting/filtering
CREATE INDEX IF NOT EXISTS idx_personas_updated_at ON public.personas(updated_at DESC);

-- Create a trigger to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_personas_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Drop trigger if it exists to avoid conflicts
DROP TRIGGER IF EXISTS trigger_personas_updated_at ON public.personas;

-- Create trigger
CREATE TRIGGER trigger_personas_updated_at
BEFORE UPDATE ON public.personas
FOR EACH ROW
EXECUTE FUNCTION update_personas_updated_at();

-- Add comment for table
COMMENT ON TABLE public.personas IS 'Stores persona definitions generated from raw text input';
COMMENT ON COLUMN public.personas.id IS 'Unique identifier (UUID v4)';
COMMENT ON COLUMN public.personas.raw_text IS 'Original unstructured text input';
COMMENT ON COLUMN public.personas.persona IS 'Structured persona JSON output';
COMMENT ON COLUMN public.personas.created_at IS 'Timestamp when persona was created';
COMMENT ON COLUMN public.personas.updated_at IS 'Timestamp when persona was last updated';
