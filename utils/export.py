"""
Export Module
Handles data export in multiple formats
"""

import json
import csv
import logging
from typing import List, Dict, Any
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Exporter:
    """Handles data export"""
    
    @staticmethod
    def export_papers_to_json(papers: List[Dict], output_path: str) -> bool:
        """Export papers to JSON"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(papers, f, indent=2, ensure_ascii=False)
            logger.info(f"Exported {len(papers)} papers to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error exporting to JSON: {e}")
            return False
    
    @staticmethod
    def export_papers_to_csv(papers: List[Dict], output_path: str) -> bool:
        """Export papers to CSV"""
        try:
            if not papers:
                logger.warning("No papers to export")
                return False
            
            fields = ["id", "pmid", "title", "abstract", "publication_date",
                     "journal", "doi", "cited_by_count", "open_access"]
            
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                for paper in papers:
                    row = {field: paper.get(field, "") for field in fields}
                    writer.writerow(row)
            
            logger.info(f"Exported {len(papers)} papers to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
            return False

exporter = Exporter()

def export_papers_to_json(papers: List[Dict], output_path: str) -> bool:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    return exporter.export_papers_to_json(papers, output_path)

def export_papers_to_csv(papers: List[Dict], output_path: str) -> bool:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    return exporter.export_papers_to_csv(papers, output_path)
