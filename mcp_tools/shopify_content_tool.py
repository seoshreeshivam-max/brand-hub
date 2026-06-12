import sys
import os

# Add the project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

import requests
from backend.auth_manager import auth_manager

class ShopifyContentTool:
    """
    Writing tool to update product content, metadata, and status.
    """
    def update_product_seo(self, brand_id: str, product_id: str, title: str = None, body_html: str = None):
        """
        Updates a product's title or body_html on Shopify.
        """
        return self._update_product(brand_id, product_id, {"title": title, "body_html": body_html})

    def update_product_status(self, brand_id: str, product_id: str, status: str):
        """
        Changes product status (active, draft, archived).
        Used for auto-drafting products with 0 stock.
        """
        if status not in ["active", "draft", "archived"]:
            raise ValueError("Invalid status. Must be active, draft, or archived.")
        return self._update_product(brand_id, product_id, {"status": status})

    def _update_product(self, brand_id: str, product_id: str, data: dict):
        """
        Internal helper for Shopify PUT requests.
        """
        token = auth_manager.get_shopify_token(brand_id)
        prefix = brand_id.upper().replace("-", "_")
        store = os.getenv(f"{prefix}_SHOPIFY_STORE") or os.getenv("SHOPIFY_STORE")
        
        url = f"https://{store}/admin/api/2024-04/products/{product_id}.json"
        
        # Filter out None values
        clean_data = {k: v for k, v in data.items() if v is not None}
        payload = {"product": {"id": product_id, **clean_data}}
            
        response = requests.put(url, json=payload, headers={"X-Shopify-Access-Token": token})
        response.raise_for_status()
        
        return response.json().get("product")

shopify_content_tool = ShopifyContentTool()
