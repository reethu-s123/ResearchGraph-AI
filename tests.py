"""
ResearchGraph AI Testing Module
Unit tests for core functionality
"""

import pytest
from backend.paper_retrieval import search_papers
from backend.nlp_processor import extract_keywords, summarize_paper
from backend.similarity_search import find_similar_by_keywords
from backend.citation_analyzer import calculate_influence_score

class TestPaperRetrieval:
    def test_search_papers_returns_list(self):
        papers = search_papers("artificial intelligence", max_results=5)
        assert isinstance(papers, list)
    
    def test_paper_has_required_fields(self):
        papers = search_papers("machine learning", max_results=1)
        if papers:
            paper = papers[0]
            assert "title" in paper
            assert "abstract" in paper

class TestNLPProcessor:
    def test_extract_keywords_returns_list(self):
        text = "Machine learning is a subset of artificial intelligence"
        keywords = extract_keywords(text, top_k=3)
        assert isinstance(keywords, list)
    
    def test_summarization_returns_string(self):
        abstract = "Machine learning has emerged as a powerful tool for solving complex problems"
        summary = summarize_paper(abstract)
        assert isinstance(summary, str)
        assert len(summary) > 0

class TestCitationAnalyzer:
    def test_influence_score_in_range(self):
        score = calculate_influence_score("test_paper")
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
