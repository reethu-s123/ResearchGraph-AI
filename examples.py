"""
Quick Start Examples for ResearchGraph AI
Demonstrates core functionality
"""

# Example 1: Basic Paper Search
def example_search():
    """Search for papers and display results"""
    from backend.paper_retrieval import search_papers
    
    papers = search_papers("machine learning", max_results=5)
    
    for i, paper in enumerate(papers, 1):
        print(f"\n{i}. {paper['title']}")
        print(f"   Authors: {len(paper['authors'])} authors")
        print(f"   Year: {paper['publication_date']}")
        print(f"   Citations: {paper['cited_by_count']}")

# Example 2: Summarization Pipeline
def example_summarization():
    """Summarize papers automatically"""
    from backend.paper_retrieval import search_papers
    from backend.nlp_processor import summarize_paper, extract_keywords
    
    papers = search_papers("deep learning", max_results=3)
    
    for paper in papers:
        print(f"\nTitle: {paper['title']}")
        summary = summarize_paper(paper['abstract'])
        print(f"Summary: {summary}")
        keywords = extract_keywords(paper['abstract'], top_k=5)
        print(f"Keywords: {', '.join(keywords)}")

# Example 3: Citation Analysis
def example_citations():
    """Analyze citation patterns"""
    from backend.paper_retrieval import search_papers
    from backend.citation_analyzer import (
        add_papers, 
        rank_papers_by_influence,
        get_research_trends
    )
    
    papers = search_papers("neural networks", max_results=10)
    add_papers(papers)
    
    influential = rank_papers_by_influence(top_k=5, method='h_index')
    print("Most Influential Papers:")
    for paper_id, score in influential:
        print(f"  - ID: {paper_id}, Score: {score:.3f}")

# Example 4: Knowledge Graph
def example_graph():
    """Build knowledge graph from papers"""
    from backend.paper_retrieval import search_papers
    from backend.graph_builder import build_from_papers, get_graph_statistics
    
    papers = search_papers("artificial intelligence", max_results=5)
    build_from_papers(papers, include_authors=True, include_methods=True)
    
    stats = get_graph_statistics()
    print(f"Graph Statistics:")
    print(f"  Nodes: {stats['total_nodes']}")
    print(f"  Edges: {stats['total_edges']}")
    print(f"  Density: {stats['density']:.3f}")

# Example 5: Export Results
def example_export():
    """Export papers to different formats"""
    from backend.paper_retrieval import search_papers
    from utils.export import export_papers_to_json, export_papers_to_csv
    
    papers = search_papers("computer vision", max_results=10)
    
    export_papers_to_json(papers, "output/papers.json")
    print("✅ Exported to JSON")
    
    export_papers_to_csv(papers, "output/papers.csv")
    print("✅ Exported to CSV")

# Example 6: Similarity Search
def example_similarity():
    """Find similar papers"""
    from backend.paper_retrieval import search_papers
    from backend.similarity_search import add_papers, find_similar
    
    papers = search_papers("machine learning", max_results=20)
    add_papers(papers)
    
    if papers:
        similar = find_similar(papers[0], top_k=5, threshold=0.6)
        print(f"Papers similar to: {papers[0]['title']}")
        for paper, score in similar:
            print(f"  - {paper['title']} (similarity: {score:.2f})")

# Example 7: Trend Analysis
def example_trends():
    """Analyze research trends"""
    from backend.paper_retrieval import search_papers
    from backend.citation_analyzer import add_papers, get_research_trends
    from backend.nlp_processor import extract_keywords
    
    papers = search_papers("neural networks", max_results=30)
    add_papers(papers)
    
    keywords = []
    for paper in papers:
        keywords.extend(extract_keywords(paper['abstract'], top_k=3))
    
    trends = get_research_trends(keywords)
    print("Publication Trends:")
    for year, count in sorted(trends['publication_trend'].items()):
        print(f"  {year}: {count} papers")

# Example 8: Complete Workflow
def example_complete_workflow():
    """Complete research analysis workflow"""
    from backend.paper_retrieval import search_papers
    from backend.nlp_processor import summarize_paper, extract_keywords
    from backend.citation_analyzer import add_papers, rank_papers_by_influence
    from backend.graph_builder import build_from_papers, get_graph_statistics
    from utils.export import export_papers_to_json
    
    print("🔍 Searching for papers...")
    papers = search_papers("artificial intelligence", max_results=10)
    
    print("📊 Building analysis...")
    add_papers(papers)
    build_from_papers(papers)
    
    print("⭐ Finding influential papers...")
    influential = rank_papers_by_influence(top_k=5)
    
    print("📈 Getting statistics...")
    stats = get_graph_statistics()
    
    print("💾 Exporting results...")
    export_papers_to_json(papers, "output/analysis.json")
    
    print("\n✅ Analysis Complete!")
    print(f"   Papers analyzed: {len(papers)}")
    print(f"   Graph nodes: {stats['total_nodes']}")
    print(f"   Graph edges: {stats['total_edges']}")

if __name__ == "__main__":
    print("ResearchGraph AI - Examples\n")
    
    # Uncomment to run examples
    # example_search()
    # example_summarization()
    # example_citations()
    # example_graph()
    # example_export()
    # example_similarity()
    # example_trends()
    example_complete_workflow()
