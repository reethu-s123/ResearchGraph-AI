"""
Citation Analyzer Module
Analyzes citation relationships and calculates influence scores
"""

from typing import List, Dict, Set, Tuple
import logging
import networkx as nx
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CitationAnalyzer:
    """Analyzes citation networks and calculates influence"""
    
    def __init__(self):
        """Initialize citation analyzer"""
        self.citation_graph = nx.DiGraph()
        self.papers = {}
    
    def add_papers(self, papers: List[Dict]) -> None:
        """
        Add papers to the citation network
        
        Args:
            papers: List of paper dictionaries
        """
        for paper in papers:
            paper_id = paper.get("id") or paper.get("pmid")
            self.papers[paper_id] = paper
            self.citation_graph.add_node(
                paper_id,
                title=paper.get("title", ""),
                year=paper.get("publication_date", 0),
                citations=paper.get("cited_by_count", 0)
            )
    
    def add_citation_relationship(self, citing_paper_id: str, cited_paper_id: str, weight: float = 1.0) -> None:
        """
        Add a citation relationship (citing_paper -> cited_paper)
        
        Args:
            citing_paper_id: ID of the paper doing the citing
            cited_paper_id: ID of the paper being cited
            weight: Edge weight
        """
        self.citation_graph.add_edge(citing_paper_id, cited_paper_id, weight=weight)
    
    def calculate_influence_score(self, paper_id: str, method: str = "pagerank") -> float:
        """
        Calculate influence score for a paper
        
        Args:
            paper_id: Paper ID
            method: Scoring method (pagerank, betweenness, degree, h-index)
        
        Returns:
            Influence score between 0 and 1
        """
        if paper_id not in self.citation_graph:
            return 0.0
        
        try:
            if method == "pagerank":
                pagerank = nx.pagerank(self.citation_graph)
                return pagerank.get(paper_id, 0.0)
            
            elif method == "betweenness":
                # Normalize betweenness centrality
                if len(self.citation_graph) > 2:
                    betweenness = nx.betweenness_centrality(self.citation_graph)
                    return betweenness.get(paper_id, 0.0)
                return 0.0
            
            elif method == "degree":
                # In-degree centrality (how many times cited)
                in_degree = self.citation_graph.in_degree(paper_id)
                max_degree = len(self.citation_graph) - 1
                return in_degree / max_degree if max_degree > 0 else 0.0
            
            elif method == "h_index":
                # H-index based scoring
                citations = self.papers.get(paper_id, {}).get("cited_by_count", 0)
                return min(1.0, citations / 1000.0)  # Normalize to [0, 1]
            
            else:
                return 0.0
        
        except Exception as e:
            logger.error(f"Error calculating influence score: {e}")
            return 0.0
    
    def rank_papers_by_influence(
        self,
        paper_ids: List[str] = None,
        method: str = "pagerank",
        top_k: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Rank papers by influence
        
        Args:
            paper_ids: List of paper IDs to rank (None = all)
            method: Ranking method
            top_k: Number of top papers to return
        
        Returns:
            List of (paper_id, score) tuples
        """
        papers_to_rank = paper_ids or list(self.papers.keys())
        
        scores = [
            (pid, self.calculate_influence_score(pid, method))
            for pid in papers_to_rank
        ]
        
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]
    
    def get_citation_chain(self, paper_id: str, depth: int = 3) -> Dict:
        """
        Get citation chain (citing and cited papers)
        
        Args:
            paper_id: Paper ID
            depth: Depth of citation chain to retrieve
        
        Returns:
            Dictionary with citing and cited papers
        """
        if paper_id not in self.citation_graph:
            return {"citing": [], "cited": []}
        
        citing_papers = []
        cited_papers = []
        
        # Get papers that cite this paper
        for node in self.citation_graph.predecessors(paper_id):
            citing_papers.append({
                "id": node,
                "title": self.citation_graph.nodes[node].get("title", ""),
                "year": self.citation_graph.nodes[node].get("year", 0)
            })
        
        # Get papers cited by this paper
        for node in self.citation_graph.successors(paper_id):
            cited_papers.append({
                "id": node,
                "title": self.citation_graph.nodes[node].get("title", ""),
                "year": self.citation_graph.nodes[node].get("year", 0)
            })
        
        return {
            "citing": citing_papers[:depth],
            "cited": cited_papers[:depth],
            "total_citing": len(list(self.citation_graph.predecessors(paper_id))),
            "total_cited": len(list(self.citation_graph.successors(paper_id)))
        }
    
    def get_research_trends(self, keywords: List[str]) -> Dict:
        """
        Get research trends for keywords by year
        
        Args:
            keywords: List of research keywords
        
        Returns:
            Dictionary with trend data
        """
        trends_by_year = defaultdict(int)
        citation_trend = defaultdict(int)
        
        for paper_id, paper in self.papers.items():
            year = paper.get("publication_date", 0)
            title = paper.get("title", "").lower()
            abstract = paper.get("abstract", "").lower()
            
            # Check if keywords match
            if any(kw.lower() in title or kw.lower() in abstract for kw in keywords):
                trends_by_year[year] += 1
                citation_trend[year] += paper.get("cited_by_count", 0)
        
        return {
            "publication_trend": dict(sorted(trends_by_year.items())),
            "citation_trend": dict(sorted(citation_trend.items())),
            "total_papers": sum(trends_by_year.values()),
            "average_citations": sum(citation_trend.values()) / max(len(citation_trend), 1)
        }
    
    def find_influential_authors(self, top_k: int = 10) -> List[Tuple[str, int]]:
        """
        Find most influential authors by citation count
        
        Args:
            top_k: Number of top authors to return
        
        Returns:
            List of (author_name, citation_count) tuples
        """
        author_citations = defaultdict(int)
        
        for paper in self.papers.values():
            citations = paper.get("cited_by_count", 0)
            for author in paper.get("authors", []):
                author_name = author.get("name", "")
                if author_name:
                    author_citations[author_name] += citations
        
        sorted_authors = sorted(author_citations.items(), key=lambda x: x[1], reverse=True)
        return sorted_authors[:top_k]
    
    def get_graph_metrics(self) -> Dict:
        """
        Get overall citation network metrics
        
        Returns:
            Dictionary with graph metrics
        """
        return {
            "total_nodes": self.citation_graph.number_of_nodes(),
            "total_edges": self.citation_graph.number_of_edges(),
            "density": nx.density(self.citation_graph),
            "average_degree": 2 * self.citation_graph.number_of_edges() / max(self.citation_graph.number_of_nodes(), 1),
            "connected_components": nx.number_weakly_connected_components(self.citation_graph)
        }


# Global instance
analyzer = CitationAnalyzer()

def add_papers(papers: List[Dict]) -> None:
    """Convenience function to add papers"""
    analyzer.add_papers(papers)

def add_citation_relationship(citing_id: str, cited_id: str, weight: float = 1.0) -> None:
    """Convenience function to add citation relationship"""
    analyzer.add_citation_relationship(citing_id, cited_id, weight)

def calculate_influence_score(paper_id: str, **kwargs) -> float:
    """Convenience function to calculate influence score"""
    return analyzer.calculate_influence_score(paper_id, **kwargs)

def rank_papers_by_influence(**kwargs) -> List[Tuple[str, float]]:
    """Convenience function to rank papers"""
    return analyzer.rank_papers_by_influence(**kwargs)

def get_citation_chain(paper_id: str, **kwargs) -> Dict:
    """Convenience function to get citation chain"""
    return analyzer.get_citation_chain(paper_id, **kwargs)

def get_research_trends(keywords: List[str]) -> Dict:
    """Convenience function to get research trends"""
    return analyzer.get_research_trends(keywords)
