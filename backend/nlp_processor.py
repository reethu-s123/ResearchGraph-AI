"""
NLP Processor Module
Handles text summarization, keyword extraction, and entity recognition
"""

import spacy
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import nltk
from nltk.tokenize import sent_tokenize
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class NLPProcessor:
    """Handles NLP tasks for research papers"""
    
    def __init__(self):
        """Initialize NLP models"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("Loaded spaCy model: en_core_web_sm")
        except OSError:
            logger.warning("spaCy model not found")
            self.nlp = None
        
        try:
            self.summarizer = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=-1
            )
            logger.info("Loaded summarization model")
        except Exception as e:
            logger.error(f"Error loading summarization model: {e}")
            self.summarizer = None
        
        try:
            self.embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
            logger.info("Loaded embedding model")
        except Exception as e:
            logger.error(f"Error loading embedding model: {e}")
            self.embedder = None
    
    def summarize_paper(self, abstract: str, max_length: int = 150, min_length: int = 80) -> str:
        """Generate 2-3 line summary of paper abstract"""
        if not abstract or len(abstract.split()) < 50:
            return abstract[:200] + "..." if len(abstract) > 200 else abstract
        
        if not self.summarizer:
            return self._fallback_summary(abstract)
        
        try:
            summary = self.summarizer(abstract, max_length=max_length, min_length=min_length, do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            logger.error(f"Error in summarization: {e}")
            return self._fallback_summary(abstract)
    
    def _fallback_summary(self, text: str, num_sentences: int = 3) -> str:
        """Fallback extractive summarization"""
        sentences = sent_tokenize(text)
        return " ".join(sentences[:num_sentences])
    
    def extract_keywords(self, text: str, top_k: int = 10) -> List[str]:
        """Extract keywords from text"""
        if not self.nlp or not text:
            return []
        
        try:
            doc = self.nlp(text.lower())
            keywords = []
            for chunk in doc.noun_chunks:
                if len(chunk.text.split()) <= 3:
                    keywords.append(chunk.text)
            keywords = list(set(keywords))[:top_k]
            return sorted(keywords)
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            return []
    
    def extract_named_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities from text"""
        if not self.nlp or not text:
            return {}
        
        try:
            doc = self.nlp(text)
            entities = {}
            for ent in doc.ents:
                if ent.label_ not in entities:
                    entities[ent.label_] = []
                entities[ent.label_].append(ent.text)
            return {k: list(set(v)) for k, v in entities.items()}
        except Exception as e:
            logger.error(f"Error extracting entities: {e}")
            return {}
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get sentence embeddings"""
        if not self.embedder or not texts:
            return []
        try:
            embeddings = self.embedder.encode(texts, convert_to_tensor=False)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return []
    
    def extract_methods(self, abstract: str) -> List[str]:
        """Extract methods from abstract"""
        method_keywords = [
            "method", "approach", "technique", "framework", "algorithm",
            "model", "analysis", "experiment", "survey", "review",
            "classification", "regression", "clustering", "deep learning"
        ]
        methods = []
        text_lower = abstract.lower()
        for keyword in method_keywords:
            if keyword in text_lower:
                methods.append(keyword)
        return methods
    
    def extract_datasets(self, abstract: str) -> List[str]:
        """Extract dataset mentions from abstract"""
        common_datasets = [
            "ImageNet", "MNIST", "CIFAR", "COCO", "Pascal VOC",
            "Wikipedia", "arXiv", "PubMed", "Reddit", "Twitter",
            "UCI Machine Learning Repository", "Kaggle"
        ]
        datasets = []
        for dataset in common_datasets:
            if dataset.lower() in abstract.lower():
                datasets.append(dataset)
        return datasets

processor = NLPProcessor()

def summarize_paper(abstract: str, **kwargs) -> str:
    return processor.summarize_paper(abstract, **kwargs)

def extract_keywords(text: str, **kwargs) -> List[str]:
    return processor.extract_keywords(text, **kwargs)

def extract_named_entities(text: str) -> Dict[str, List[str]]:
    return processor.extract_named_entities(text)

def get_embeddings(texts: List[str]) -> List[List[float]]:
    return processor.get_embeddings(texts)

def extract_methods(abstract: str) -> List[str]:
    return processor.extract_methods(abstract)

def extract_datasets(abstract: str) -> List[str]:
    return processor.extract_datasets(abstract)
