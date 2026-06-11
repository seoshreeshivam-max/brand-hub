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
    The Investigative Agent: Correlates Search drops with Retail issues.
    """
    def investigate_anomaly(self, brand_id: str, brand_config: dict):
        """
        Deep dive into a brand's data to find the root cause of an anomaly.
        """
        print(f"[AuditorAgent] Investigating {brand_id}...")
        
        # 1. Check Product Health (Inventory/Metadata)
        product_health = shopify_audit_tool.get_product_seo_health(brand_id)
        
        # 2. Identify major issues
        out_of_stock = [p for p in product_health if "OUT_OF_STOCK" in p["issues"]]
        thin_content = [p for p in product_health if "THIN_CONTENT" in p["issues"]]
        
        # 3. Formulate Hypothesis
        hypothesis = "Stable"
        if out_of_stock:
            hypothesis = f"Potential Revenue Drop: {len(out_of_stock)} top products are Out of Stock."
        elif thin_content:
            hypothesis = f"SEO Risk: {len(thin_content)} products have thin descriptions (<100 chars)."
        
        return {
            "brand_id": brand_id,
            "findings": {
                "out_of_stock_count": len(out_of_stock),
                "thin_content_count": len(thin_content),
                "sample_issues": product_health[:3]
            },
            "hypothesis": hypothesis,
            "recommended_action": "Restock top sellers" if out_of_stock else "Enhance product descriptions"
        }

auditor_agent = AuditorAgent()
