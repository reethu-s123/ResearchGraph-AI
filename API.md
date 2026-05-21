"""
ResearchGraph AI - API Reference
Complete documentation of all modules and functions
"""

# API REFERENCE

## Backend Module: paper_retrieval

### search_papers(query, max_results=50, year_from=None, year_to=None, sort_by='relevance')
Search scientific papers from Europe PMC.

**Parameters:**
- `query` (str): Search keywords
- `max_results` (int): Maximum papers to return
- `year_from` (int, optional): Start year filter
- `year_to` (int, optional): End year filter
- `sort_by` (str): Sort order ('relevance', 'date_asc', 'date_desc')

**Returns:** List[Dict] - List of paper dictionaries

**Example:**
```python
papers = search_papers("deep learning", max_results=20, year_from=2020)
```

### get_paper_details(pmid)
Get detailed information about a specific paper.

**Parameters:**
- `pmid` (str): PubMed ID

**Returns:** Dict - Paper details

**Example:**
```python
paper = get_paper_details("12345678")
```

### get_citations(pmid)
Get papers citing a specific paper.

**Parameters:**
- `pmid` (str): PubMed ID of the source paper

**Returns:** List[Dict] - List of citing papers

---

## Backend Module: nlp_processor

### summarize_paper(abstract, max_length=150, min_length=80)
Generate concise summary of paper abstract.

**Parameters:**
- `abstract` (str): Paper abstract text
- `max_length` (int): Maximum summary length
- `min_length` (int): Minimum summary length

**Returns:** str - Summarized text

**Example:**
```python
summary = summarize_paper(paper['abstract'])
print(summary)  # 2-3 line summary
```

### extract_keywords(text, top_k=10)
Extract key topics from text.

**Parameters:**
- `text` (str): Input text
- `top_k` (int): Number of keywords to return

**Returns:** List[str] - List of keywords

**Example:**
```python
keywords = extract_keywords(abstract, top_k=5)
# Returns: ['machine learning', 'neural networks', ...]
```

### extract_named_entities(text)
Extract named entities (person, org, location, etc.).

**Parameters:**
- `text` (str): Input text

**Returns:** Dict[str, List[str]] - Entity types and values

**Example:**
```python
entities = extract_named_entities(abstract)
# Returns: {'PERSON': ['John Doe'], 'ORG': ['MIT'], ...}
```

### extract_methods(abstract)
Identify research methods mentioned.

**Parameters:**
- `abstract` (str): Paper abstract

**Returns:** List[str] - Methods used

### extract_datasets(abstract)
Identify datasets mentioned.

**Parameters:**
- `abstract` (str): Paper abstract

**Returns:** List[str] - Datasets used

### get_embeddings(texts)
Generate semantic embeddings for texts.

**Parameters:**
- `texts` (List[str]): List of text strings

**Returns:** List[List[float]] - Embedding vectors

---

## Backend Module: similarity_search

### add_papers(papers)
Add papers to similarity search index.

**Parameters:**
- `papers` (List[Dict]): Papers with abstracts

### find_similar(query_paper, top_k=10, threshold=0.7)
Find papers similar to query paper.

**Parameters:**
- `query_paper` (Dict): Reference paper
- `top_k` (int): Number of results
- `threshold` (float): Minimum similarity score

**Returns:** List[Tuple[Dict, float]] - Similar papers and scores

**Example:**
```python
similar = find_similar(papers[0], top_k=5, threshold=0.6)
for paper, score in similar:
    print(f"{paper['title']} ({score:.2f})")
```

### find_similar_by_keywords(keywords, papers, top_k=10, threshold=0.3)
Find papers by keyword overlap.

**Parameters:**
- `keywords` (List[str]): Query keywords
- `papers` (List[Dict]): Candidate papers
- `top_k` (int): Number of results
- `threshold` (float): Minimum overlap ratio

**Returns:** List[Tuple[Dict, float]] - Matching papers and scores

---

## Backend Module: citation_analyzer

### add_papers(papers)
Add papers to citation network.

**Parameters:**
- `papers` (List[Dict]): Papers with citation data

### calculate_influence_score(paper_id, method='pagerank')
Calculate paper's influence score.

**Parameters:**
- `paper_id` (str): Paper identifier
- `method` (str): Scoring method ('pagerank', 'betweenness', 'degree', 'h_index')

**Returns:** float - Influence score (0.0 to 1.0)

**Example:**
```python
score = calculate_influence_score("paper_123", method='h_index')
```

### rank_papers_by_influence(paper_ids=None, method='pagerank', top_k=10)
Rank papers by influence.

**Parameters:**
- `paper_ids` (List[str], optional): Papers to rank (all if None)
- `method` (str): Ranking method
- `top_k` (int): Number of top papers

**Returns:** List[Tuple[str, float]] - Ranked papers and scores

### get_citation_chain(paper_id, depth=3)
Get papers citing and cited by a paper.

**Parameters:**
- `paper_id` (str): Paper identifier
- `depth` (int): Chain depth

**Returns:** Dict - Citation chain data

### get_research_trends(keywords)
Get publication and citation trends for keywords.

**Parameters:**
- `keywords` (List[str]): Research topics

**Returns:** Dict - Trend data by year

---

## Backend Module: graph_builder

### build_from_papers(papers, include_authors=True, include_methods=True, include_datasets=True)
Build knowledge graph from papers.

**Parameters:**
- `papers` (List[Dict]): Input papers
- `include_authors` (bool): Include author nodes
- `include_methods` (bool): Include method nodes
- `include_datasets` (bool): Include dataset nodes

**Example:**
```python
build_from_papers(papers, include_authors=True, include_methods=True)
```

### get_graph_statistics()
Get knowledge graph statistics.

**Returns:** Dict - Graph metrics and statistics

### get_subgraph(node_id, depth=2)
Get subgraph around a node.

**Parameters:**
- `node_id` (str): Center node
- `depth` (int): Maximum distance

**Returns:** NetworkX graph object

### export_to_json(output_path=None)
Export graph to JSON.

**Parameters:**
- `output_path` (str, optional): Output file path

**Returns:** str - JSON string

---

## Utilities Module: export

### export_papers_to_json(papers, output_path)
Export papers to JSON file.

### export_papers_to_csv(papers, output_path)
Export papers to CSV file.

### export_analysis_to_json(papers, trends, influential_papers, output_path)
Export comprehensive analysis.

---

## Utilities Module: cache

### get_cached(key)
Retrieve value from cache.

**Returns:** Any or None if not found

### set_cache(key, value)
Store value in cache.

**Returns:** bool - Success status

### clear_cache()
Clear all cached data.

**Returns:** bool - Success status

---

## Data Structures

### Paper Dictionary
```python
{
    "id": "string",
    "pmid": "string",
    "title": "string",
    "abstract": "string",
    "authors": [
        {
            "name": "string",
            "affiliation": "string"
        }
    ],
    "publication_date": int,
    "journal": "string",
    "doi": "string",
    "cited_by_count": int,
    "open_access": bool,
    "keywords": ["string"],
    "mesh_terms": ["string"],
    "source_url": "string"
}
```

### Influence Score (0.0 to 1.0)
- 0.0: No influence
- 0.5: Moderate influence
- 1.0: Highest influence

### Similarity Score (0.0 to 1.0)
- 0.0: Not similar
- 0.5: Moderately similar
- 1.0: Identical
