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
    Writing tool to update product content and metadata.
    """
    def update_product_seo(self, brand_id: str, product_id: str, title: str = None, body_html: str = None):
        """
        Updates a product's title or body_html on Shopify.
        """
        token = auth_manager.get_shopify_token(brand_id)
        prefix = brand_id.upper().replace("-", "_")
        store = os.getenv(f"{prefix}_SHOPIFY_STORE") or os.getenv("SHOPIFY_STORE")
        
        url = f"https://{store}/admin/api/2024-04/products/{product_id}.json"
        
        payload = {"product": {"id": product_id}}
        if title:
            payload["product"]["title"] = title
        if body_html:
            payload["product"]["body_html"] = body_html
            
        response = requests.put(url, json=payload, headers={"X-Shopify-Access-Token": token})
        response.raise_for_status()
        
        return response.json().get("product")

shopify_content_tool = ShopifyContentTool()
