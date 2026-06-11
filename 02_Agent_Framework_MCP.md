# Component: Agent Framework & Model Context Protocol (MCP)

This is the "brain" of the hub. Instead of writing rigid scripts for every task, we will define **Tools** and let LLMs orchestrate the workflows.

## 1. Model Context Protocol (MCP) Integration
MCP allows us to standardize how agents interact with our data connectors.
*   **Standardized Tools:** We will expose our Data Connectors (01_Data_Connectors) as MCP Tools.
    *   *Example Tool:* `get_gsc_queries(brand_id: str, date_range: str)`
    *   *Example Tool:* `update_shopify_product_seo(brand_id: str, product_id: str, meta_title: str)`
*   **LLM Flexibility:** By using MCP, we can easily swap between high-efficiency models like **Claude Sonnet 4.6** and high-reasoning frontier models like **Claude Fable 5** (the current standard for complex task decomposition).

## 2. Agent Orchestration (AI SDK / SDK)
We will utilize the **Vercel AI SDK** or a specialized **Agent SDK** for orchestration. This provides a more robust and type-safe structure compared to legacy frameworks like CrewAI, allowing for better streaming, tool-calling management, and state persistence.

### Agent Persona Expansion
In addition to core executors, we will implement agents for cross-verification:

*   **The Auditor Agent:**
    *   *Role:* Reviews the output of the Content Creator Agent against SEO guidelines and brand voice.
    *   *Tools:* Brand Voice Guidelines (Local PDF/Markdown), SEO Checklist tool.
*   **The Monitor Agent:**
    *   *Role:* Continuously polls GSC and GA4 for anomalies (e.g., sudden traffic drops or indexing errors) and alerts the team or triggers other agents.
    *   *Tools:* GSC API, Slack/Webhook Notification tool.
*   **The SEO Analyst Agent:** ...

    *   *Tools:* GSC API, GA4 API, DataForSEO.
    *   *Task:* Detect ranking drops, identify new keyword opportunities across brands.
*   **The Content Creator Agent:**
    *   *Tools:* Firecrawl (competitor research), Shopify API (drafting).
    *   *Task:* Write and publish agentic content based on the Analyst's findings.
*   **The E-commerce Manager Agent:**
    *   *Tools:* GMC API, Shopify API.
    *   *Task:* Resolve product disapprovals in Merchant Center, optimize product titles.

## 3. Migration from `shree_seo_engine`
*   Existing Python scripts in `shree_seo_engine` (like `audit_article.py`, `seo-auto-update.py`) will be refactored into modular MCP Tools.
*   The rigid execution flow will be replaced by Agent Prompts that dynamically decide which tools to use.

## Note:
* We need to add the multiple agents for the cross checks and auditing, monitoring etc 