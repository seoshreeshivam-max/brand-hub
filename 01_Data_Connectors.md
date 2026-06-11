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
