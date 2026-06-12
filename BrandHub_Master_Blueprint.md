# Omni-Brand AI Hub: Master Architecture (hub.shreeshivam.com)

## 1. Vision & Overview
A centralized, agentic control center designed to operate multiple brands (Shree Shivam, White Hanger, Mynk, etc.) from a single unified interface. It will ingest data from Google APIs and CMS backends, and utilize LLM agents via Model Context Protocol (MCP) to automate SEO, content, and e-commerce operations.

## 2. Core Tenets
*   **Multi-Tenant by Design:** Every action, API call, and database query requires a `brand_id` context. (we can use domains as brandid)
*   **Agent-Driven (MCP):** Heavy reliance on autonomous agents rather than static scripts. Agents will have access to "Tools" (APIs) defined via the Model Context Protocol.
*   **Modular Extensibility:** Built on top of the successes of the `shree_seo_engine`, but refactored to be platform-agnostic.

## 3. High-Level Architecture Flow
1.  **Frontend (The Hub):** A modern web app (e.g., Next.js or Streamlit) where operators select a brand via a global dropdown. (will prefrer next.js or whichever is best with speed)
2.  **API Gateway / Orchestrator:** Routes requests to the appropriate brand's configuration and triggers the necessary agents.
3.  **Data Layer (Connectors):**
    *   Google Ecosystem: GA4, GSC, GMC APIs.
    *   E-commerce/CMS: Shopify Admin API, custom backends.
    *   External Intelligence: DataForSEO, Serper, Firecrawl. (serper is costly we can utilise the other options https://www.reddit.com/r/Agentic_SEO/s/bYpLWyzpTv)
4.  **Agent Layer:** Agents built using specific **ADK/SDK Agent Orchestration** (replacing legacy frameworks like CrewAI) equipped with MCP tools to execute workflows (e.g., "Analyze drops in White Hanger GSC and draft new content via Shopify API").
5.  **Token & Cost Management Layer:** A dedicated middleware to optimize API calls, manage tokens across multiple models (Claude Sonnet 4.6, Fable 5), and ensure cost-efficient operations.

## 4. Next Steps
*   Review component documents for specific implementations.
*   Set up initial authentication and brand configuration schemas.
*   Port existing functional logic from `shree_seo_engine` into the new MCP tool format.
*   Implement the Token Manager for cost optimization.
# Component: Data Connectors & Integrations

This module handles all external API communication. To support multi-brand operations, all connectors must accept a configuration object (credentials, properties, scope) rather than relying on hardcoded `.env` variables.

## 1. Google Ecosystem Integrations
*   **Google Search Console (GSC) API:**
    *   *Purpose:* Fetch keyword rankings, indexing status, and click data.
    *   *Brand Config:* Requires specific Property URIs per brand.
*   **Google Analytics 4 (GA4) API:**
    *   *Purpose:* Track user behavior, conversions, and page performance.
    *   *Brand Config:* Requires specific Property IDs per brand.
*   **Google Merchant Center (GMC) API:**
    *   *Purpose:* Sync product feeds, check product approval status, and fix merchant errors.
    *   *Brand Config:* Requires specific Merchant IDs per brand.

## 2. CMS & E-commerce Backends
*   **Shopify Admin API (GraphQL/REST):**
    *   *Purpose:* Read/Write products, update metadata, publish blog posts, manage redirects.
    *   *Brand Config:* Requires distinct Store URLs and Access Tokens per brand.
*   **ONDC / Custom Backends:**
    *   *Purpose:* Sync inventory, manage multi-channel listings.

## 3. External Intelligence APIs (Reddit /Agentic_SEO Stack)
*   **DataForSEO:** Primary choice for cost-effective, high-volume SERP data, keywords, and backlink metrics.
*   **Alternatives (Cost Optimization):** Utilize cheaper scraping options from the Agentic_SEO community (e.g., ValueSerp, SearchApi) instead of high-cost providers like Serper.io where possible.
*   **Firecrawl / Jina Reader:** To fetch live URLs and convert them to clean Markdown for LLM ingestion.
*   **Ahrefs / Semrush (Optional):** For enterprise backlink and domain authority metrics.

## 4. Implementation Strategy
*   Create a central `credentials_manager.py` that loads the correct API keys based on the active brand selection.
*   Wrap all Google/Shopify API calls in standardized Python classes (e.g., `BrandGSCClient(brand_id)`).
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
# Component: Frontend Hub (hub.shreeshivam.com)

The user interface for human operators to oversee the autonomous agents and manual workflows.

## 1. Core UI Elements
*   **Global Brand Selector:** A persistent top-nav dropdown to switch context between:
    *   Shree Shivam
    *   White Hanger
    *   Mynk
    *   (Add New Brand...)
*   **Dashboard / Overview:**
    *   Aggregated health metrics for the selected brand (GSC Clicks, GA4 Sessions, GMC Active Products).
*   **Agent Control Center:**
    *   View active agent runs (e.g., "Content Agent currently drafting 5 articles for Mynk").
    *   Approval queues (Human-in-the-loop for reviewing content before Shopify publish).
    *   Chat interface to interact directly with the brand's data (e.g., "Why did White Hanger traffic drop yesterday?").

## 2. Technology Stack Recommendations
*   **Frontend Framework:** Next.js (React) with Tailwind CSS for a highly polished, enterprise feel, OR Streamlit if rapid internal development is the priority.
*   **Backend / API:** FastAPI (Python) to serve as the bridge between the Frontend and the Agent Framework/MCP layer.
*   **Database:** PostgreSQL or SQLite to store agent run logs, user sessions, and brand configurations. (Parquet will be better with rust?)

## 3. Workflow Example (UI Perspective)
1.  User logs in and selects "Mynk" from the dropdown.
2.  User navigates to the "Agent Chat".
3.  User types: "Audit our top 10 co-ord sets and optimize their SEO titles based on current SERP intent."
4.  UI shows the Agent executing steps: fetching from Shopify -> querying Serper.io -> rewriting -> pushing to Shopify.
5.  UI presents a summary of the 10 changed titles.
# Component: Token & Cost Manager

To ensure the hub remains cost-effective while operating three brands, we require a centralized token management system.

## 1. Multi-Model Token Routing
*   **Dynamic Routing:** Logic to route simple tasks (e.g., "Summarize this GSC report") to cost-efficient models (Claude Sonnet 4.6) and complex reasoning tasks (e.g., "Create a 3-month strategy for Mynk") to frontier models (Claude Fable 5).
*   **Fallback Logic:** Automatically switch to a secondary model if a primary model hits rate limits or latency spikes.

## 2. Usage Tracking & Budgeting
*   **Brand-Level Quotas:** Assign token budgets to each brand (Shree Shivam, White Hanger, Mynk) to prevent one brand from consuming the entire monthly API budget.
*   **Real-time Cost Dashboard:** Integrate with the Frontend Hub to show exactly how much each brand has spent on LLM and SEO APIs (DataForSEO, Serper, etc.).

## 3. Optimization Strategies
*   **Prompt Caching:** Utilize model-specific prompt caching features to reduce costs for repetitive system prompts and large context windows (like product catalogs).
*   **Context Pruning:** Agents will use tools to "summarize and prune" context before sending it to the LLM, ensuring only relevant data is processed.
*   **Batch Processing:** For non-urgent tasks (e.g., bulk product SEO updates), utilize "Batch API" modes offered by providers to save up to 50% on costs.

## 4. Implementation Details
*   Develop a `cost_monitor.py` that intercepts all `model_generate` calls and logs token counts (input/output) to the database.
*   Create a configuration file `token_configs.json` where admins can set thresholds and active model overrides.
