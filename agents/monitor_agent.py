import sys
import os

# Add the project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from mcp_tools.gsc_fetcher import gsc_fetcher
from mcp_tools.shopify_fetcher import shopify_fetcher
import json

class MonitorAgent:
    """
    The GSC & Shopify Monitor Agent: Oversees SEO and Retail health across all brands.
    """
    def __init__(self, brands_config_path: str):
        with open(brands_config_path, "r") as f:
            self.brands = json.load(f)["brands"]

    def run_daily_audit(self):
        """
        Executes a performance audit for all active brands.
        """
        results = {}
        for brand in self.brands:
            if brand["status"] == "active":
                print(f"[MonitorAgent] Auditing {brand['name']}...")
                try:
                    # 1. Fetch SEO Data
                    seo_data = gsc_fetcher.get_performance_summary(brand["gsc_property"])
                    latest_row = seo_data[-1] if seo_data else None
                    
                    # 2. Fetch Shopify Data
                    retail_data = shopify_fetcher.get_sales_summary(brand["id"])
                    
                    # Basic Anomaly Check
                    status = "healthy"
                    if (latest_row and latest_row['clicks'] == 0) or (retail_data['order_count'] == 0):
                        status = "anomaly_detected"
                    
                    results[brand["id"]] = {
                        "name": brand["name"],
                        "status": status,
                        "seo": {
                            "latest_clicks": latest_row['clicks'] if latest_row else 0,
                            "latest_date": latest_row['keys'][0] if latest_row else "N/A"
                        },
                        "retail": retail_data
                    }
                except Exception as e:
                    results[brand["id"]] = {"name": brand["name"], "status": "error", "error": str(e)}
        
        return results

# Example usage
if __name__ == "__main__":
    CONFIG_PATH = os.path.join(BASE_DIR, "config", "brands.json")
    agent = MonitorAgent(CONFIG_PATH)
    report = agent.run_daily_audit()
    print(json.dumps(report, indent=2))
