import os
from dotenv import load_dotenv
from supabase import create_client, Client, ClientOptions

load_dotenv()

# --- Supabase Client ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables are missing. Please provide them.")

options = ClientOptions(postgrest_client_timeout=120, storage_client_timeout=120)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY, options=options)
