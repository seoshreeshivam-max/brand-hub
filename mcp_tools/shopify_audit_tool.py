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
    Advanced Diagnostic tool for product health, inventory sync, and category depth.
    """
    def get_product_seo_health(self, brand_id: str, product_id: str = None):
        """
        Audits products for:
        - Status vs Stock sync (Stock > 0 should be live, 0 should be draft)
        - Deep details (Category/Product Type, Title, Name)
        - SEO thickness
        """
        token = auth_manager.get_shopify_token(brand_id)
        prefix = brand_id.upper().replace("-", "_")
        store = os.getenv(f"{prefix}_SHOPIFY_STORE") or os.getenv("SHOPIFY_STORE")
        
        # Fetch products with extended fields
        url = f"https://{store}/admin/api/2024-04/products.json?limit=20"
        if product_id:
            url = f"https://{store}/admin/api/2024-04/products/{product_id}.json"
            
        response = requests.get(url, headers={"X-Shopify-Access-Token": token})
        response.raise_for_status()
        products = response.json().get("products", [response.json().get("product")])
        
        audit_results = []
        for p in products:
            if not p: continue
            
            # Check inventory across all variants
            total_inventory = sum(v.get("inventory_quantity", 0) for v in p.get("variants", []))
            current_status = p.get("status") # active, draft, or archived
            product_type = p.get("product_type") # Category
            
            issues = []
            recommendations = []
            
            # Rule: Stock > 0 -> Active; Stock == 0 -> Draft
            if total_inventory > 0 and current_status != "active":
                issues.append("STOCK_AVAILABLE_BUT_DRAFT")
                recommendations.append("SET_TO_LIVE")
            elif total_inventory <= 0 and current_status == "active":
                issues.append("LIVE_BUT_OUT_OF_STOCK")
                recommendations.append("MOVE_TO_DRAFT")
                
            if len(p.get("body_html", "")) < 100:
                issues.append("THIN_CONTENT")
            
            audit_results.append({
                "id": p["id"],
                "name": p["title"],
                "category": product_type or "Uncategorized",
                "status": current_status,
                "inventory": total_inventory,
                "issues": issues,
                "recommendations": recommendations,
                "vendor": p.get("vendor"),
                "tags": p.get("tags")
            })
            
        return audit_results

shopify_audit_tool = ShopifyAuditTool()
