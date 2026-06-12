import sys
import os

# Add the project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from mcp_tools.shopify_audit_tool import shopify_audit_tool
from mcp_tools.gsc_fetcher import gsc_fetcher
import json

class AuditorAgent:
    """
    The Investigative Agent: Correlates Search drops with Retail and Inventory Status.
    Now supports deep category (Product Type) analysis and status-stock sync logic.
    """
    def investigate_anomaly(self, brand_id: str, brand_config: dict):
        """
        Deep dive into a brand's data to find the root cause of an anomaly.
        """
        print(f"[AuditorAgent] Investigating {brand_id} with Inventory-Status Sync check...")
        
        # 1. Check Product Health (Inventory, Metadata, Category, Status)
        product_health = shopify_audit_tool.get_product_seo_health(brand_id)
        
        # 2. Identify major issues based on user business rules
        out_of_sync = [p for p in product_health if "LIVE_BUT_OUT_OF_STOCK" in p["issues"] or "STOCK_AVAILABLE_BUT_DRAFT" in p["issues"]]
        thin_content = [p for p in product_health if "THIN_CONTENT" in p["issues"]]
        
        # 3. Formulate Hypothesis
        hypothesis = "Stable"
        recommended_action = "No immediate action required"
        
        if out_of_sync:
            count = len(out_of_sync)
            hypothesis = f"Inventory Sync Alert: {count} products have status-stock mismatches."
            recommended_action = "Auto-Draft OOS products & Publish Restocked items"
        elif thin_content:
            hypothesis = f"SEO Risk: {len(thin_content)} products have thin descriptions (<100 chars)."
            recommended_action = "Enhance product descriptions with Content Agent"
        
        return {
            "brand_id": brand_id,
            "findings": {
                "out_of_sync_count": len(out_of_sync),
                "thin_content_count": len(thin_content),
                "sample_issues": product_health[:5] # Includes category and vendor now
            },
            "hypothesis": hypothesis,
            "recommended_action": recommended_action,
            "can_auto_fix": len(out_of_sync) > 0
        }

auditor_agent = AuditorAgent()
