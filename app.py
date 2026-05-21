"""
ResearchGraph AI - Main Streamlit Application
Real-time scientific literature assistant
"""

import streamlit as st
import json
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict

# Import backend modules
from backend.paper_retrieval import search_papers, get_paper_details
from backend.nlp_processor import summarize_paper, extract_keywords, extract_methods, extract_datasets
from backend.similarity_search import find_similar, find_similar_by_keywords, add_papers
from backend.citation_analyzer import (
    add_papers as add_papers_citation,
    calculate_influence_score,
    rank_papers_by_influence,
    get_research_trends
)
from backend.graph_builder import build_from_papers, get_graph_statistics, export_to_json
from utils.export import export_papers_to_json, export_papers_to_csv, export_analysis_to_json
from utils.cache import get_cached, set_cache, clear_cache

# Page configuration
st.set_page_config(
    page_title="ResearchGraph AI 🔬📚",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .summary-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-left: 4px solid #0066cc;
        margin-bottom: 1rem;
    }
    .trend-container {
        background-color: #fff5e6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "papers" not in st.session_state:
    st.session_state.papers = []
if "selected_paper" not in st.session_state:
    st.session_state.selected_paper = None
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = {}

def load_papers(query: str, max_results: int = 50) -> List[Dict]:
    """Load papers with caching"""
    cache_key = f"papers_{query}_{max_results}"
    
    # Check cache
    cached_papers = get_cached(cache_key)
    if cached_papers:
        st.success("📦 Results loaded from cache")
        return cached_papers
    
    # Fetch from API
    with st.spinner(f"🔍 Searching for papers about '{query}'..."):
        papers = search_papers(query, max_results=max_results)
    
    if papers:
        set_cache(cache_key, papers)
        st.success(f"✅ Found {len(papers)} papers")
        return papers
    else:
        st.error("❌ No papers found")
        return []

def display_paper_card(paper: Dict, index: int) -> None:
    """Display individual paper card"""
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader(f"📄 {paper.get('title', 'Untitled')}")
            
            # Metadata
            meta_cols = st.columns(4)
            with meta_cols[0]:
                st.caption(f"📅 {paper.get('publication_date', 'N/A')}")
            with meta_cols[1]:
                st.caption(f"👨‍💼 {len(paper.get('authors', []))} authors")
            with meta_cols[2]:
                st.caption(f"📎 {paper.get('cited_by_count', 0)} citations")
            with meta_cols[3]:
                if paper.get('open_access'):
                    st.caption("🔓 Open Access")
            
            # Summary
            abstract = paper.get('abstract', '')
            if abstract:
                summary = summarize_paper(abstract)
                st.markdown(f"<div class='summary-box'><strong>Summary:</strong> {summary}</div>", unsafe_allow_html=True)
            
            # Keywords and Methods
            keywords = extract_keywords(abstract, top_k=5)
            methods = extract_methods(abstract)
            datasets = extract_datasets(abstract)
            
            info_cols = st.columns(3)
            if keywords:
                with info_cols[0]:
                    st.caption("🏷️ **Keywords**")
                    st.text(", ".join(keywords))
            if methods:
                with info_cols[1]:
                    st.caption("🔧 **Methods**")
                    st.text(", ".join(methods))
            if datasets:
                with info_cols[2]:
                    st.caption("📊 **Datasets**")
                    st.text(", ".join(datasets))
        
        with col2:
            if st.button("👁️ View", key=f"view_{index}"):
                st.session_state.selected_paper = paper
            
            if paper.get('source_url'):
                st.link_button("🔗 Open", paper['source_url'])
            
            influence = calculate_influence_score(paper.get('id') or paper.get('pmid'), method='h_index')
            st.metric("Influence", f"{influence:.2f}")
    
    st.divider()

def display_knowledge_graph_stats() -> None:
    """Display knowledge graph statistics"""
    if st.session_state.papers:
        build_from_papers(st.session_state.papers, include_authors=True, include_methods=True, include_datasets=True)
        stats = get_graph_statistics()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Nodes", stats.get('total_nodes', 0))
        with col2:
            st.metric("Total Edges", stats.get('total_edges', 0))
        with col3:
            st.metric("Graph Density", f"{stats.get('density', 0):.3f}")
        with col4:
            st.metric("Avg Degree", f"{stats.get('average_degree', 0):.2f}")
        
        # Node types distribution
        node_types = stats.get('node_types', {})
        if node_types:
            fig = px.pie(
                values=list(node_types.values()),
                names=list(node_types.keys()),
                title="Node Types Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)

def display_trends() -> None:
    """Display research trends"""
    if st.session_state.papers:
        add_papers_citation(st.session_state.papers)
        
        keywords = []
        for paper in st.session_state.papers:
            keywords.extend(extract_keywords(paper.get('abstract', ''), top_k=3))
        
        if keywords:
            trends = get_research_trends(keywords)
            
            # Publication trend
            pub_trend = trends.get('publication_trend', {})
            if pub_trend:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=list(pub_trend.keys()),
                    y=list(pub_trend.values()),
                    mode='lines+markers',
                    name='Publications',
                    line=dict(color='#0066cc', width=3)
                ))
                fig.update_layout(
                    title="Publication Trend Over Time",
                    xaxis_title="Year",
                    yaxis_title="Number of Papers",
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Citation trend
            citation_trend = trends.get('citation_trend', {})
            if citation_trend:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=list(citation_trend.keys()),
                    y=list(citation_trend.values()),
                    name='Citations',
                    marker_color='#ff6b6b'
                ))
                fig.update_layout(
                    title="Citation Trend Over Time",
                    xaxis_title="Year",
                    yaxis_title="Total Citations"
                )
                st.plotly_chart(fig, use_container_width=True)

# Main UI
st.title("🔬 ResearchGraph AI")
st.markdown("**Scientific Paper Summarization, Citation Linking, and Knowledge Graph Builder**")

# Sidebar
with st.sidebar:
    st.header("⚙️ Controls")
    
    # Search section
    st.subheader("🔍 Search Papers")
    search_query = st.text_input("Enter research topic:", placeholder="e.g., machine learning")
    max_results = st.slider("Max results:", 10, 100, 20)
    
    if st.button("Search", use_container_width=True):
        st.session_state.papers = load_papers(search_query, max_results)
    
    st.divider()
    
    # Utility section
    st.subheader("📁 Export & Cache")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Export JSON", use_container_width=True):
            if st.session_state.papers:
                export_papers_to_json(st.session_state.papers, "output/papers.json")
                st.success("Exported to papers.json")
    with col2:
        if st.button("📊 Export CSV", use_container_width=True):
            if st.session_state.papers:
                export_papers_to_csv(st.session_state.papers, "output/papers.csv")
                st.success("Exported to papers.csv")
    
    if st.button("🧹 Clear Cache", use_container_width=True):
        clear_cache()
        st.success("Cache cleared!")

# Main content
if not st.session_state.papers:
    st.info("👋 Start by searching for research papers on the left sidebar")
else:
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📄 Papers",
        "📊 Analysis",
        "🌐 Knowledge Graph",
        "📈 Trends",
        "💡 Insights"
    ])
    
    with tab1:
        st.subheader(f"Found {len(st.session_state.papers)} Papers")
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            sort_by = st.selectbox("Sort by:", ["Relevance", "Citations", "Date"])
        with col2:
            show_open_access = st.checkbox("Open Access Only", value=False)
        
        # Display papers
        filtered_papers = st.session_state.papers
        if show_open_access:
            filtered_papers = [p for p in filtered_papers if p.get('open_access')]
        
        for i, paper in enumerate(filtered_papers):
            display_paper_card(paper, i)
    
    with tab2:
        st.subheader("📊 Analysis Summary")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Papers", len(st.session_state.papers))
        with col2:
            avg_citations = sum(p.get('cited_by_count', 0) for p in st.session_state.papers) / len(st.session_state.papers)
            st.metric("Avg Citations", f"{avg_citations:.1f}")
        with col3:
            open_access_count = sum(1 for p in st.session_state.papers if p.get('open_access'))
            st.metric("Open Access", f"{open_access_count}/{len(st.session_state.papers)}")
        
        # Top influential papers
        st.subheader("⭐ Most Influential Papers")
        add_papers_citation(st.session_state.papers)
        influential = rank_papers_by_influence(top_k=5, method='h_index')
        
        for paper_id, score in influential:
            for paper in st.session_state.papers:
                if (paper.get('id') or paper.get('pmid')) == paper_id:
                    col1, col2 = st.columns([4, 1]
                    with col1:
                        st.write(f"**{paper.get('title', 'Untitled')}**")
                    with col2:
                        st.metric("Score", f"{score:.3f}")
                    break
    
    with tab3:
        st.subheader("🌐 Knowledge Graph")
        display_knowledge_graph_stats()
        
        if st.button("📥 Export Graph as JSON"):
            graph_json = export_to_json()
            st.download_button(
                label="Download Graph JSON",
                data=graph_json,
                file_name="knowledge_graph.json",
                mime="application/json"
            )
    
    with tab4:
        st.subheader("📈 Research Trends")
        display_trends()
    
    with tab5:
        st.subheader("💡 Key Insights")
        
        # Extract common methods
        all_methods = []
        for paper in st.session_state.papers:
            all_methods.extend(extract_methods(paper.get('abstract', '')))
        
        method_counts = {}
        for method in all_methods:
            method_counts[method] = method_counts.get(method, 0) + 1
        
        if method_counts:
            st.write("**Most Common Methods:**")
            methods_df = pd.DataFrame(
                sorted(method_counts.items(), key=lambda x: x[1], reverse=True)[:10],
                columns=["Method", "Count"]
            )
            fig = px.bar(methods_df, x="Method", y="Count", title="Method Frequency")
            st.plotly_chart(fig, use_container_width=True)
        
        # Extract common datasets
        all_datasets = []
        for paper in st.session_state.papers:
            all_datasets.extend(extract_datasets(paper.get('abstract', '')))
        
        dataset_counts = {}
        for dataset in all_datasets:
            dataset_counts[dataset] = dataset_counts.get(dataset, 0) + 1
        
        if dataset_counts:
            st.write("**Most Used Datasets:**")
            datasets_df = pd.DataFrame(
                sorted(dataset_counts.items(), key=lambda x: x[1], reverse=True),
                columns=["Dataset", "Count"]
            )
            fig = px.bar(datasets_df, x="Dataset", y="Count", title="Dataset Frequency")
            st.plotly_chart(fig, use_container_width=True)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.85rem;'>
    <p>ResearchGraph AI v1.0 | Built with Python, Streamlit, and 🧠 NLP</p>
    <p>Data from Europe PMC • Open Science Initiative</p>
</div>
""", unsafe_allow_html=True)
