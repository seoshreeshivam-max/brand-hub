import sys
import os

# Add the project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

import requests
from backend.auth_manager import auth_manager

class ShopifyFetcher:
    """
    MCP-compatible tool for fetching e-commerce metrics from Shopify.
    """
    
    def get_sales_summary(self, brand_id: str):
        """
        Fetches recent order counts and total sales volume.
        """
        token = auth_manager.get_shopify_token(brand_id)
        
        prefix = brand_id.upper().replace("-", "_")
        store = os.getenv(f"{prefix}_SHOPIFY_STORE") or os.getenv("SHOPIFY_STORE")
        
        url = f"https://{store}/admin/api/2024-04/orders.json?status=any&limit=50"
        headers = {"X-Shopify-Access-Token": token}
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        orders = response.json().get("orders", [])
        
        total_sales = sum(float(order["total_price"]) for order in orders)
        order_count = len(orders)
        
        return {
            "total_sales": round(total_sales, 2),
            "order_count": order_count,
            "currency": orders[0]["currency"] if orders else "INR"
        }

shopify_fetcher = ShopifyFetcher()
