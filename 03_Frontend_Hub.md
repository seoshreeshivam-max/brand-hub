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
