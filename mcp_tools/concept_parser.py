import sys
import os

# Add the project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

class ConceptParserTool:
    """
    MCP Tool: Agentic Context Parsing.
    Shifts from traditional exact-match Search Volume (SV) to aggregated 'Concept Volume' 
    based on semantic entities, user intent, and KGMID mapping.
    """
    def parse_concept(self, seed_topic: str):
        """
        Analyzes a seed topic and groups semantic variations into a unified Concept Volume.
        """
        print(f"[MCP: ConceptParser] Aggregating concept cluster for: '{seed_topic}'")
        
        # In production, this tool will:
        # 1. Fetch 500+ related keywords via DataForSEO.
        # 2. Scrape top 5 SERP pages via Firecrawl to analyze semantic overlap.
        # 3. Use an LLM to prune outliers and group the remaining terms into a Concept.
        
        # Simulated Agentic Output for Demo
        # (Assuming the seed_topic was something like "party wear lehenga")
        
        aggregated_data = {
            "seed_topic": seed_topic,
            "primary_entity_concept": f"{seed_topic.title()} & Occasion Wear",
            "metrics": {
                "traditional_exact_sv": 2400,
                "agentic_concept_volume": 18500,  # The true addressable traffic
                "estimated_cpc_value": "$4.50"
            },
            "intent_profile": {
                "transactional": "65%",
                "informational": "25%",
                "navigational": "10%"
            },
            "semantic_clusters": [
                {"sub_topic": f"Buy {seed_topic} online", "contribution_sv": 5500, "intent": "Transactional"},
                {"sub_topic": f"Best {seed_topic} designs 2026", "contribution_sv": 4200, "intent": "Informational"},
                {"sub_topic": f"{seed_topic} for wedding reception", "contribution_sv": 6400, "intent": "Transactional"}
            ],
            "agent_directive": f"Do not target exact match. Build a pillar page (or rich collection page) covering the 3 semantic clusters to capture the full 18.5k Concept Volume."
        }
        
        return aggregated_data

concept_parser = ConceptParserTool()
