"""
Similarity Search Module
Find similar papers using embeddings and keyword overlap
"""

from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimilaritySearch:
    """Handles paper similarity search"""
    
    def __init__(self, embedding_model=None):
        """Initialize similarity search"""
        self.embedding_model = embedding_model
        self.paper_embeddings = {}
    
    def add_papers(self, papers: List[Dict]) -> None:
        """
        Add papers and compute embeddings
        
        Args:
            papers: List of paper dictionaries with abstracts
        """
        if not self.embedding_model:
            logger.warning("No embedding model available")
            return
        
        try:
            abstracts = [p.get("abstract", "") for p in papers if p.get("abstract")]
            
            if not abstracts:
                logger.warning("No abstracts found")
                return
            
            # Get embeddings for all abstracts
            embeddings = self.embedding_model.encode(abstracts, convert_to_tensor=False)
            
            # Store embeddings mapped to paper IDs
            for paper, embedding in zip(papers, embeddings):
                self.paper_embeddings[paper["id"]] = {
                    "embedding": embedding,
                    "paper": paper
                }
            
            logger.info(f"Added embeddings for {len(papers)} papers")
        
        except Exception as e:
            logger.error(f"Error adding papers: {e}")
    
    def find_similar(
        self,
        query_paper: Dict,
        top_k: int = 10,
        threshold: float = 0.7
    ) -> List[Tuple[Dict, float]]:
        """
        Find similar papers to a query paper
        
        Args:
            query_paper: Reference paper dictionary
            top_k: Number of similar papers to return
            threshold: Minimum similarity score
        
        Returns:
            List of (paper, similarity_score) tuples
        """
        if not self.embedding_model or not self.paper_embeddings:
            logger.warning("Cannot perform similarity search")
            return []
        
        try:
            # Get embedding for query paper
            query_abstract = query_paper.get("abstract", "")
            if not query_abstract:
                return []
            
            query_embedding = self.embedding_model.encode(
                query_abstract,
                convert_to_tensor=False
            )
            
            # Calculate similarities with all stored papers
            similarities = []
            for paper_id, data in self.paper_embeddings.items():
                if data["paper"]["id"] != query_paper["id"]:  # Skip self
                    similarity = cosine_similarity(
                        [query_embedding],
                        [data["embedding"]]
                    )[0][0]
                    
                    if similarity >= threshold:
                        similarities.append((data["paper"], similarity))
            
            # Sort by similarity and return top_k
            similarities.sort(key=lambda x: x[1], reverse=True)
            return similarities[:top_k]
        
        except Exception as e:
            logger.error(f"Error finding similar papers: {e}")
            return []
    
    def find_similar_by_keywords(
        self,
        keywords: List[str],
        papers: List[Dict],
        top_k: int = 10,
        threshold: float = 0.3
    ) -> List[Tuple[Dict, float]]:
        """
        Find papers similar by keyword overlap
        
        Args:
            keywords: Query keywords
            papers: Candidate papers
            top_k: Number of papers to return
            threshold: Minimum overlap ratio
        
        Returns:
            List of (paper, similarity_score) tuples
        """
        keyword_set = set(k.lower() for k in keywords)
        results = []
        
        for paper in papers:
            # Combine title, abstract, and keywords
            paper_text = (
                paper.get("title", "") + " " +
                paper.get("abstract", "") + " " +
                " ".join(paper.get("keywords", []))
            ).lower()
            
            # Count keyword matches
            matches = sum(1 for kw in keyword_set if kw in paper_text)
            similarity = matches / max(len(keyword_set), 1)
            
            if similarity >= threshold:
                results.append((paper, similarity))
        
        # Sort and return top_k
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
    
    def get_paper_cluster(
        self,
        papers: List[Dict],
        threshold: float = 0.6,
        method: str = "embeddings"
    ) -> Dict[int, List[Dict]]:
        """
        Cluster similar papers
        
        Args:
            papers: List of papers to cluster
            threshold: Similarity threshold for clustering
            method: Clustering method (embeddings or keywords)
        
        Returns:
            Dictionary mapping cluster ID to papers
        """
        if not papers:
            return {}
        
        clusters = {}
        cluster_id = 0
        assigned = set()
        
        for i, paper in enumerate(papers):
            if i in assigned:
                continue
            
            clusters[cluster_id] = [paper]
            assigned.add(i)
            
            # Find similar papers
            if method == "embeddings":
                similar = self.find_similar(paper, top_k=len(papers), threshold=threshold)
            else:
                keywords = paper.get("keywords", [])
                similar = self.find_similar_by_keywords(keywords, papers, top_k=len(papers), threshold=threshold)
            
            for similar_paper, _ in similar:
                for j, p in enumerate(papers):
                    if p["id"] == similar_paper["id"] and j not in assigned:
                        clusters[cluster_id].append(p)
                        assigned.add(j)
            
            cluster_id += 1
        
        return clusters


# Global instance
similarity_search = SimilaritySearch()

def add_papers(papers: List[Dict]) -> None:
    """Convenience function to add papers"""
    similarity_search.add_papers(papers)

def find_similar(query_paper: Dict, **kwargs) -> List[Tuple[Dict, float]]:
    """Convenience function to find similar papers"""
    return similarity_search.find_similar(query_paper, **kwargs)

def find_similar_by_keywords(keywords: List[str], papers: List[Dict], **kwargs) -> List[Tuple[Dict, float]]:
    """Convenience function to find similar papers by keywords"""
    return similarity_search.find_similar_by_keywords(keywords, papers, **kwargs)
