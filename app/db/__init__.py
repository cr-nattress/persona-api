"""
Database module with Supabase client and database utilities.
"""

from .supabase_client import get_supabase_client, reset_supabase_client, SupabaseClient

__all__ = [
    "get_supabase_client",
    "reset_supabase_client",
    "SupabaseClient",
]
