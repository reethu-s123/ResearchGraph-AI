"""
Knowledge Graph Builder Module
Constructs and visualizes knowledge graphs from research papers
"""

import networkx as nx
import json
from typing import List, Dict, Tuple, Set
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KnowledgeGraphBuilder:
    """Builds and manages knowledge graphs"""
    
    def __init__(self):
        """Initialize graph builder"""
        self.graph = nx.MultiDiGraph()
        self.papers = {}
        self.entities = {}
    
    def add_paper_node(self, paper: Dict) -> None:
        """
        Add a paper as a node
        
        Args:
            paper: Paper dictionary
        """
        paper_id = paper.get("id") or paper.get("pmid")
        self.graph.add_node(
            paper_id,
            node_type="paper",
            title=paper.get("title", ""),
            year=paper.get("publication_date", 0),
            citations=paper.get("cited_by_count", 0),
            doi=paper.get("doi", ""),
            url=paper.get("source_url", "")
        )
        self.papers[paper_id] = paper
    
    def add_entity_node(self, entity_id: str, entity_type: str, label: str, attributes: Dict = None) -> None:
        """
        Add an entity node (author, method, dataset, etc.)
        
        Args:
            entity_id: Unique entity identifier
            entity_type: Type of entity (author, method, dataset, venue)
            label: Display label
            attributes: Additional attributes
        """
        node_attributes = {
            "node_type": entity_type,
            "label": label,
            **(attributes or {})
        }
        self.graph.add_node(entity_id, **node_attributes)
        self.entities[entity_id] = node_attributes
    
    def add_relationship(
        self,
        source_id: str,
        target_id: str,
        relationship_type: str,
        weight: float = 1.0,
        attributes: Dict = None
    ) -> None:
        """
        Add a relationship edge
        
        Args:
            source_id: Source node ID
            target_id: Target node ID
            relationship_type: Type of relationship
            weight: Edge weight
            attributes: Additional attributes
        """
        edge_attributes = {
            "relationship_type": relationship_type,
            "weight": weight,
            **(attributes or {})
        }
        self.graph.add_edge(source_id, target_id, **edge_attributes)
    
    def build_from_papers(
        self,
        papers: List[Dict],
        include_authors: bool = True,
        include_methods: bool = True,
        include_datasets: bool = True
    ) -> None:
        """
        Build knowledge graph from papers
        
        Args:
            papers: List of paper dictionaries
            include_authors: Include author nodes and relationships
            include_methods: Include method nodes and relationships
            include_datasets: Include dataset nodes and relationships
        """
        try:
            # Add paper nodes
            for paper in papers:
                self.add_paper_node(paper)
            
            # Add author nodes and relationships
            if include_authors:
                for paper in papers:
                    paper_id = paper.get("id") or paper.get("pmid")
                    for author in paper.get("authors", []):
                        author_name = author.get("name", "")
                        if author_name:
                            author_id = f"author_{author_name.replace(' ', '_')}"
                            self.add_entity_node(
                                author_id,
                                "author",
                                author_name,
                                {"affiliation": author.get("affiliation", "")}
                            )
                            self.add_relationship(
                                paper_id,
                                author_id,
                                "authored_by",
                                weight=1.0
                            )
            
            # Add method nodes and relationships
            if include_methods:
                from backend.nlp_processor import extract_methods
                for paper in papers:
                    paper_id = paper.get("id") or paper.get("pmid")
                    abstract = paper.get("abstract", "")
                    methods = extract_methods(abstract)
                    for method in methods:
                        method_id = f"method_{method.replace(' ', '_')}"
                        self.add_entity_node(method_id, "method", method)
                        self.add_relationship(
                            paper_id,
                            method_id,
                            "uses_method",
                            weight=1.0
                        )
            
            # Add dataset nodes and relationships
            if include_datasets:
                from backend.nlp_processor import extract_datasets
                for paper in papers:
                    paper_id = paper.get("id") or paper.get("pmid")
                    abstract = paper.get("abstract", "")
                    datasets = extract_datasets(abstract)
                    for dataset in datasets:
                        dataset_id = f"dataset_{dataset.replace(' ', '_')}"
                        self.add_entity_node(dataset_id, "dataset", dataset)
                        self.add_relationship(
                            paper_id,
                            dataset_id,
                            "uses_dataset",
                            weight=1.0
                        )
            
            # Add citation relationships
            for paper in papers:
                paper_id = paper.get("id") or paper.get("pmid")
                # Note: Would need actual citation data from API
                # This is a placeholder for the structure
            
            logger.info(f"Built knowledge graph with {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges")
        
        except Exception as e:
            logger.error(f"Error building knowledge graph: {e}")
    
    def get_subgraph(self, node_id: str, depth: int = 2) -> nx.MultiDiGraph:
        """
        Get subgraph around a node
        
        Args:
            node_id: Center node ID
            depth: Maximum distance from center node
        
        Returns:
            Subgraph
        """
        if node_id not in self.graph:
            return nx.MultiDiGraph()
        
        subgraph_nodes = {node_id}
        current_nodes = {node_id}
        
        for _ in range(depth):
            next_nodes = set()
            for node in current_nodes:
                # Add neighbors
                for neighbor in self.graph.neighbors(node):
                    next_nodes.add(neighbor)
                for predecessor in self.graph.predecessors(node):
                    next_nodes.add(predecessor)
            
            subgraph_nodes.update(next_nodes)
            current_nodes = next_nodes
        
        return self.graph.subgraph(subgraph_nodes)
    
    def get_node_details(self, node_id: str) -> Dict:
        """
        Get detailed information about a node
        
        Args:
            node_id: Node ID
        
        Returns:
            Node details
        """
        if node_id not in self.graph:
            return {}
        
        node_data = dict(self.graph.nodes[node_id])
        
        return {
            "node_id": node_id,
            "attributes": node_data,
            "in_degree": self.graph.in_degree(node_id),
            "out_degree": self.graph.out_degree(node_id),
            "incoming_edges": [
                {
                    "source": src,
                    "type": edge_data.get("relationship_type", ""),
                    "weight": edge_data.get("weight", 1.0)
                }
                for src, _, edge_data in self.graph.in_edges(node_id, data=True)
            ],
            "outgoing_edges": [
                {
                    "target": tgt,
                    "type": edge_data.get("relationship_type", ""),
                    "weight": edge_data.get("weight", 1.0)
                }
                for _, tgt, edge_data in self.graph.out_edges(node_id, data=True)
            ]
        }
    
    def export_to_json(self, output_path: str = None) -> str:
        """
        Export graph to JSON format (node-link format)
        
        Args:
            output_path: Path to save JSON file
        
        Returns:
            JSON string
        """
        try:
            graph_dict = nx.node_link_data(self.graph)
            json_str = json.dumps(graph_dict, indent=2)
            
            if output_path:
                with open(output_path, 'w') as f:
                    f.write(json_str)
                logger.info(f"Exported graph to {output_path}")
            
            return json_str
        except Exception as e:
            logger.error(f"Error exporting graph: {e}")
            return "{}"
    
    def export_to_gexf(self, output_path: str) -> None:
        """
        Export graph to GEXF format (Gephi compatible)
        
        Args:
            output_path: Path to save GEXF file
        """
        try:
            nx.write_gexf(self.graph, output_path)
            logger.info(f"Exported graph to {output_path}")
        except Exception as e:
            logger.error(f"Error exporting GEXF: {e}")
    
    def get_graph_statistics(self) -> Dict:
        """
        Get graph statistics
        
        Returns:
            Dictionary with statistics
        """
        return {
            "total_nodes": self.graph.number_of_nodes(),
            "total_edges": self.graph.number_of_edges(),
            "density": nx.density(self.graph),
            "node_types": self._count_node_types(),
            "relationship_types": self._count_relationship_types(),
            "average_degree": 2 * self.graph.number_of_edges() / max(self.graph.number_of_nodes(), 1),
            "is_directed": self.graph.is_directed()
        }
    
    def _count_node_types(self) -> Dict[str, int]:
        """Count nodes by type"""
        counts = {}
        for node, data in self.graph.nodes(data=True):
            node_type = data.get("node_type", "unknown")
            counts[node_type] = counts.get(node_type, 0) + 1
        return counts
    
    def _count_relationship_types(self) -> Dict[str, int]:
        """Count edges by relationship type"""
        counts = {}
        for _, _, data in self.graph.edges(data=True):
            rel_type = data.get("relationship_type", "unknown")
            counts[rel_type] = counts.get(rel_type, 0) + 1
        return counts


# Global instance
graph_builder = KnowledgeGraphBuilder()

def build_from_papers(papers: List[Dict], **kwargs) -> None:
    """Convenience function to build graph"""
    graph_builder.build_from_papers(papers, **kwargs)

def get_subgraph(node_id: str, **kwargs) -> nx.MultiDiGraph:
    """Convenience function to get subgraph"""
    return graph_builder.get_subgraph(node_id, **kwargs)

def export_to_json(**kwargs) -> str:
    """Convenience function to export to JSON"""
    return graph_builder.export_to_json(**kwargs)

def get_graph_statistics() -> Dict:
    """Convenience function to get statistics"""
    return graph_builder.get_graph_statistics()
