import sys
import os

# Add the project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from mcp_tools.shopify_content_tool import shopify_content_tool
from mcp_tools.competitor_fetcher import competitor_fetcher
from backend.token_manager import token_manager
import json

class ContentAgent:
    """
    The Content Agent: Generates SEO-optimized content with Competitor Intelligence.
    """
    def generate_product_fix(self, brand_id: str, product_data: dict):
        """
        Drafts a new SEO title and description by analyzing SERP competitors.
        """
        print(f"[ContentAgent] Analyzing competitors for product {product_data.get('id')}...")
        
        # 1. Fetch Competitor Intel
        query = product_data.get("title", "Ethnic Wear")
        competitors = competitor_fetcher.get_serp_competitors(query)
        comp_titles = [c["title"] for c in competitors]
        
        # 2. Advanced Prompting Logic (Simulated for Claude Fable 5)
        current_title = product_data.get("title", "Unknown Product")
        new_title = f"{current_title} | Premium Designer Collection | {brand_id.capitalize()}"
        
        if "Wedding" in str(comp_titles):
            new_title = f"{current_title} - Beyond Wedding Guest Glamour | {brand_id.capitalize()}"

        new_body_html = f"<p>Stand out from the crowd. While competitors focus only on wedding wear, the <strong>{current_title}</strong> from {brand_id.capitalize()} is designed for versatile luxury.</p>"
        
        token_manager.track_call(brand_id, "claude-fable-5", 800, 1500)
        
        return {
            "product_id": product_data.get("id"),
            "original_title": current_title,
            "suggested_title": new_title,
            "suggested_body_html": new_body_html,
            "competitor_context": comp_titles[:3]
        }

    def apply_fix(self, brand_id: str, product_id: str, title: str, body_html: str):
        """
        Pushes the generated content to Shopify.
        """
        return shopify_content_tool.update_product_seo(brand_id, product_id, title, body_html)

content_agent = ContentAgent()
