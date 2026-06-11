import sys
import os

# Add the project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

import requests
from backend.auth_manager import auth_manager

class ShopifyAuditTool:
    """
    Diagnostic tool to check product health and metadata consistency.
    """
    def get_product_seo_health(self, brand_id: str, product_id: str = None):
        """
        Audits products for missing SEO titles, descriptions, or out-of-stock status.
        """
        token = auth_manager.get_shopify_token(brand_id)
        prefix = brand_id.upper().replace("-", "_")
        store = os.getenv(f"{prefix}_SHOPIFY_STORE") or os.getenv("SHOPIFY_STORE")
        
        # If no product_id, fetch latest 10 products for audit
        url = f"https://{store}/admin/api/2024-04/products.json?limit=10"
        if product_id:
            url = f"https://{store}/admin/api/2024-04/products/{product_id}.json"
            
        response = requests.get(url, headers={"X-Shopify-Access-Token": token})
        response.raise_for_status()
        products = response.json().get("products", [response.json().get("product")])
        
        audit_results = []
        for p in products:
            if not p: continue
            
            # Check inventory
            total_inventory = sum(v.get("inventory_quantity", 0) for v in p.get("variants", []))
            
            # Check SEO Metadata (via Metafields - simplified for v0.0)
            issues = []
            if total_inventory == 0:
                issues.append("OUT_OF_STOCK")
            if len(p.get("body_html", "")) < 100:
                issues.append("THIN_CONTENT")
            
            audit_results.append({
                "id": p["id"],
                "title": p["title"],
                "status": p["status"],
                "inventory": total_inventory,
                "issues": issues
            })
            
        return audit_results

shopify_audit_tool = ShopifyAuditTool()
