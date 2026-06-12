# BrandHub v1.0: MCP (Model Context Protocol) Architecture

To achieve "ultra-automation" using the **Vercel AI SDK**, your Python backend must act as an **MCP Server**. This server exposes your legacy scripts and API connections as standardized "Tools" that LLMs (like Claude Fable 5) can natively understand and call.

Below is the grouped structure of the required MCPs, designed as JSON schemas ready to be ingested by the AI SDK.

---

## 🛍️ Group 1: E-Commerce & CMS (Shopify)
*Tools for reading and manipulating store data, inventory, and content.*

```json
{
  "group": "shopify_cms",
  "tools": [
    {
      "name": "shopify_fetch_products",
      "description": "Fetches products, their inventory levels, and current metadata.",
      "parameters": {
        "brand_id": "string (e.g., 'shreeshivam', 'amchoor')",
        "collection_id": "string (optional)",
        "limit": "integer"
      }
    },
    {
      "name": "shopify_update_metadata",
      "description": "Updates SEO title, body_html, and alt-text for a specific product.",
      "parameters": {
        "brand_id": "string",
        "product_id": "string",
        "seo_title": "string",
        "body_html": "string",
        "alt_text_mapping": "object (image_id to alt_text)"
      }
    },
    {
      "name": "shopify_sync_inventory_status",
      "description": "Toggles product status to 'draft' if stock is 0, or 'active' if restocked.",
      "parameters": {
        "brand_id": "string",
        "product_id": "string",
        "target_status": "string ('active' | 'draft')"
      }
    },
    {
      "name": "shopify_publish_blog",
      "description": "Pushes a drafted SEO article to the Shopify Blog.",
      "parameters": {
        "brand_id": "string",
        "title": "string",
        "html_content": "string",
        "author": "string",
        "tags": "array of strings"
      }
    }
  ]
}
```

---

## 📈 Group 2: Google Ecosystem (Visibility & Analytics)
*Tools for measuring SEO health, traffic, and index coverage.*

```json
{
  "group": "google_ecosystem",
  "tools": [
    {
      "name": "gsc_fetch_performance",
      "description": "Pulls clicks, impressions, CTR, and average position for a property.",
      "parameters": {
        "brand_id": "string",
        "date_range_days": "integer",
        "dimension": "string ('date' | 'query' | 'page')"
      }
    },
    {
      "name": "gsc_inspect_url",
      "description": "Checks if a specific URL is indexed by Google.",
      "parameters": {
        "brand_id": "string",
        "url": "string"
      }
    },
    {
      "name": "ga4_fetch_metrics",
      "description": "Fetches landing page sessions, bounce rate, and conversion data.",
      "parameters": {
        "brand_id": "string",
        "path_prefix": "string (e.g., '/collections/lehengas')"
      }
    },
    {
      "name": "gmc_check_status",
      "description": "Checks Google Merchant Center for disapproved products or warnings.",
      "parameters": {
        "brand_id": "string"
      }
    }
  ]
}
```

---

## 🧠 Group 3: Strategic Intelligence (DataForSEO)
*Tools for competitor gap analysis and real-time SERP understanding.*

```json
{
  "group": "strategic_intelligence",
  "tools": [
    {
      "name": "serp_analyze_competitors",
      "description": "Fetches the top 10 organic results for a keyword to analyze competitor intent.",
      "parameters": {
        "keyword": "string",
        "location": "string (default: India)"
      }
    },
    {
      "name": "keyword_fetch_volume",
      "description": "Retrieves search volume, CPC, and competition difficulty for keyword clusters.",
      "parameters": {
        "keywords": "array of strings"
      }
    }
  ]
}
```

---

## 📓 Group 4: Notion Workspace (Planning & CRM)
*Tools to sync the dashboard UI with the team's underlying Notion databases.*

```json
{
  "group": "notion_workspace",
  "tools": [
    {
      "name": "notion_fetch_calendar",
      "description": "Pulls pending content tasks from the Content Calendar database.",
      "parameters": {
        "status_filter": "string (e.g., 'To Do', 'In Progress')"
      }
    },
    {
      "name": "notion_query_crm",
      "description": "Fetches local outreach targets (e.g., Wedding Planners) for backlink campaigns.",
      "parameters": {
        "category": "string"
      }
    },
    {
      "name": "notion_update_task",
      "description": "Updates a Notion task status once an Agent successfully publishes content.",
      "parameters": {
        "page_id": "string",
        "new_status": "string"
      }
    }
  ]
}
```

---

## ⚙️ Group 5: Advanced & Technical (ONDC & Schema)
*Tools handling highly technical injections and marketplace syncing.*

```json
{
  "group": "advanced_technical",
  "tools": [
    {
      "name": "ondc_push_inventory",
      "description": "Syncs eligible active Shopify inventory directly to the ONDC bridge.",
      "parameters": {
        "brand_id": "string",
        "product_ids": "array of strings"
      }
    },
    {
      "name": "kgmid_inject_schema",
      "description": "Generates and injects specialized JSON-LD/KGMID Schema markup into a page's metadata.",
      "parameters": {
        "brand_id": "string",
        "entity_type": "string (e.g., 'Product', 'Article')",
        "target_url": "string",
        "schema_payload": "object"
      }
    }
  ]
}
```

## How the AI SDK uses this:
When an event occurs on the frontend (e.g., User clicks "Start AI Fix"), the Vercel AI SDK sends a prompt to Claude Fable 5, providing this entire JSON list of tools. 

Claude will autonomously decide:
1. *"I need to call `shopify_fetch_products` to see the current title."*
2. *"I need to call `serp_analyze_competitors` to see what Kalki Fashion is doing."*
3. *"I need to call `shopify_update_metadata` to push the winning rewrite."*

The AI SDK handles the routing of these requests to your FastAPI backend, executing your legacy Python scripts seamlessly.
