"""
Paper Retrieval Module - Europe PMC Integration
Fetches scientific papers and metadata in real-time
"""

import requests
import json
from typing import List, Dict, Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PaperRetriever:
    """Handles paper retrieval from Europe PMC"""
    
    BASE_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session = requests.Session()
    
    def search_papers(
        self,
        query: str,
        max_results: int = 50,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        sort_by: str = "relevance"
    ) -> List[Dict]:
        """
        Search for papers using Europe PMC API
        
        Args:
            query: Search query string
            max_results: Maximum number of results
            year_from: Filter from year
            year_to: Filter to year
            sort_by: Sort results by (relevance, date_asc, date_desc)
        
        Returns:
            List of paper dictionaries
        """
        try:
            params = {
                "query": query,
                "pageSize": min(max_results, 1000),
                "format": "json",
                "sortBy": sort_by,
            }
            
            if year_from:
                params["yearFrom"] = year_from
            if year_to:
                params["yearTo"] = year_to
            
            response = self.session.get(
                f"{self.BASE_URL}/search",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            papers = []
            
            for result in data.get("resultList", {}).get("result", []):
                paper = self._parse_paper(result)
                papers.append(paper)
            
            logger.info(f"Retrieved {len(papers)} papers for query: {query}")
            return papers
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching papers: {e}")
            return []
    
    def get_paper_details(self, pmid: str) -> Optional[Dict]:
        """
        Get detailed information about a specific paper
        
        Args:
            pmid: PubMed ID of the paper
        
        Returns:
            Paper details dictionary
        """
        try:
            params = {
                "query": f"EXT_ID:{pmid}",
                "format": "json",
            }
            
            response = self.session.get(
                f"{self.BASE_URL}/search",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            results = data.get("resultList", {}).get("result", [])
            
            if results:
                return self._parse_paper(results[0])
            return None
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching paper details: {e}")
            return None
    
    def get_citations(self, pmid: str) -> List[Dict]:
        """
        Get citations for a specific paper
        
        Args:
            pmid: PubMed ID of the paper
        
        Returns:
            List of citing papers
        """
        try:
            params = {
                "query": pmid,
                "pageSize": 100,
                "format": "json",
            }
            
            response = self.session.get(
                f"{self.BASE_URL}/citations",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            citations = []
            
            for result in data.get("resultList", {}).get("result", []):
                citation = self._parse_paper(result)
                citations.append(citation)
            
            return citations
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching citations: {e}")
            return []
    
    @staticmethod
    def _parse_paper(result: Dict) -> Dict:
        """Parse paper data from API response"""
        return {
            "id": result.get("id"),
            "pmid": result.get("pmid"),
            "title": result.get("title", ""),
            "abstract": result.get("abstractText", ""),
            "authors": [
                {
                    "name": author.get("fullName", ""),
                    "affiliation": author.get("affiliation", "")
                }
                for author in result.get("authorList", {}).get("author", [])
            ],
            "publication_date": result.get("pubYear"),
            "journal": result.get("journalInfo", {}).get("journal", {}).get("title", ""),
            "doi": result.get("doi"),
            "cited_by_count": result.get("citedByCount", 0),
            "open_access": result.get("isOpenAccess", False),
            "keywords": result.get("keywordList", {}).get("keyword", []),
            "mesh_terms": result.get("meshHeadingList", []),
            "source_url": f"https://www.ncbi.nlm.nih.gov/pubmed/{result.get('pmid')}"
        }


# Global instance
retriever = PaperRetriever()

def search_papers(query: str, max_results: int = 50, **kwargs) -> List[Dict]:
    """Convenience function to search papers"""
    return retriever.search_papers(query, max_results, **kwargs)

def get_paper_details(pmid: str) -> Optional[Dict]:
    """Convenience function to get paper details"""
    return retriever.get_paper_details(pmid)

def get_citations(pmid: str) -> List[Dict]:
    """Convenience function to get citations"""
    return retriever.get_citations(pmid)
