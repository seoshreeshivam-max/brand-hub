import sys
import os

# Add the project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from googleapiclient.discovery import build
from backend.auth_manager import auth_manager
from datetime import datetime, timedelta

class GSCFetcher:
    """
    MCP-compatible tool for fetching data from Google Search Console.
    """
    def __init__(self):
        from google.oauth2.credentials import Credentials
        token = os.getenv("GSC_TOKEN")
        if token:
            self.creds = Credentials(token=token)
        else:
            self.creds = auth_manager.get_google_creds()
            
        self.service = build('searchconsole', 'v1', credentials=self.creds)

    def get_performance_summary(self, site_url: str, days: int = 7):
        """
        Fetches clicks, impressions, CTR, and position for a given site.
        """
        end_date = datetime.now() - timedelta(days=3) # GSC data is usually 2-3 days delayed
        start_date = end_date - timedelta(days=days)
        
        request = {
            'startDate': start_date.strftime('%Y-%m-%d'),
            'endDate': end_date.strftime('%Y-%m-%d'),
            'dimensions': ['date'],
            'rowLimit': 100
        }
        
        response = self.service.searchanalytics().query(siteUrl=site_url, body=request).execute()
        return response.get('rows', [])

    def get_top_query_drops(self, site_url: str, threshold: float = 0.2):
        """
        Identifies queries with significant click drops compared to the previous period.
        """
        pass

gsc_fetcher = GSCFetcher()
