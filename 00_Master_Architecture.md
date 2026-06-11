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
