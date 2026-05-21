"""ResearchGraph AI Backend Package"""

__version__ = "1.0.0"
__author__ = "Reethu S"

from backend.paper_retrieval import search_papers, get_paper_details
from backend.nlp_processor import summarize_paper, extract_keywords
from backend.citation_analyzer import calculate_influence_score
from backend.graph_builder import build_knowledge_graph

__all__ = [
    "search_papers",
    "get_paper_details",
    "summarize_paper",
    "extract_keywords",
    "calculate_influence_score",
    "build_knowledge_graph",
]
