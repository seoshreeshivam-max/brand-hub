import json
import os
from datetime import datetime, timedelta, timezone
import requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from dotenv import load_dotenv

# Load .env from project root
load_dotenv()

class AuthManager:
    """
    Centralized Auth Manager for brandHub.
    Prioritizes environment variables for Vercel compatibility.
    """
    
    @staticmethod
    def get_google_creds():
        """
        Refreshes and returns Google OAuth2 credentials from ENV or Local File.
        """
        token_json = os.getenv("GOOGLE_TOKEN_JSON")
        
        if token_json:
            # Vercel Path: Load from environment variable string
            creds_data = json.loads(token_json)
            creds = Credentials.from_authorized_user_info(creds_data)
        else:
            # Local Dev Path: Fallback to local file if ENV not set
            local_path = r"C:\Users\shree\OneDrive\Documents\mynk\Credentials\gmail_token.json"
            if os.path.exists(local_path):
                creds = Credentials.from_authorized_user_file(local_path)
            else:
                raise RuntimeError("Google Credentials not found in ENV or local file.")
        
        if creds and creds.expired and creds.refresh_token:
            print("[INFO] Refreshing Google OAuth token...")
            creds.refresh(Request())
            # In local dev, we might want to update the file, 
            # but on Vercel we just keep the refreshed object in memory.
            # (Note: Vercel env vars are read-only at runtime)
        
        return creds

    @staticmethod
    def get_shopify_token(brand_id: str):
        """
        Gets Shopify access token for a specific brand from ENV.
        """
        prefix = brand_id.upper().replace("-", "_")
        
        store = os.getenv(f"{prefix}_SHOPIFY_STORE") or os.getenv("SHOPIFY_STORE")
        client_id = os.getenv(f"{prefix}_SHOPIFY_CLIENT_ID") or os.getenv("SHOPIFY_CLIENT_ID")
        client_secret = os.getenv(f"{prefix}_SHOPIFY_CLIENT_SECRET") or os.getenv("SHOPIFY_CLIENT_SECRET")

        if not all([store, client_id, client_secret]):
            raise RuntimeError(f"Shopify credentials missing for brand: {brand_id}")

        # Basic logic: fetch a fresh token
        # (On Vercel, we'd ideally use a Redis cache for tokens, but for v.0.0 we'll fetch per session)
        url = f"https://{store}/admin/oauth/access_token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        }
        response = requests.post(url, data=payload, timeout=20)
        response.raise_for_status()
        return response.json()["access_token"]

auth_manager = AuthManager()
