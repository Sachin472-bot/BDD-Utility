from typing import Dict, Any, Optional
import re
import spacy
from docx import Document
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

class DocumentTypeIdentifier:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError as e:
            logger.error(f"Failed to load spaCy model: {str(e)}")
            raise RuntimeError("Failed to initialize document type identifier. Please ensure spaCy model is installed.")
            
        self.patterns = {
            "BRD": [
                r"business\s+requirements?\s+documents?",
                r"stakeholder\s+requirements?",
                r"business\s+needs?",
                r"business\s+objectives?",
                r"scope\s+and\s+limitations?"
            ],
            "FRD": [
                r"functional\s+requirements?\s+documents?",
                r"system\s+requirements?",
                r"functional\s+specifications?",
                r"technical\s+requirements?",
                r"system\s+functionality"
            ],
            "User Story": [
                r"as\s+an?\s+.*\s+i\s+want\s+to",
                r"as\s+an?\s+.*\s+i\s+need\s+to",
                r"as\s+an?\s+.*\s+i\s+should\s+be\s+able\s+to",
                r"given.*when.*then",
                r"acceptance\s+criteria"
            ],
            "Test Case": [
                r"test\s+cases?",
                r"test\s+scenarios?",
                r"steps?\s+to\s+test",
                r"expected\s+results?",
                r"preconditions?",
                r"test\s+data"
            ]
        }

    def identify_document_type(self, content: str) -> Dict[str, float]:
        """
        Analyze document content and return confidence scores for each document type.
        Returns a dictionary of document types and their confidence scores.
        """
        doc = self.nlp(content.lower())
        scores = {doc_type: 0.0 for doc_type in self.patterns.keys()}
        
        # Calculate scores based on pattern matches
        for doc_type, patterns in self.patterns.items():
            matches = 0
            for pattern in patterns:
                if re.search(pattern, content.lower()):
                    matches += 1
            scores[doc_type] = matches / len(patterns)
        
        # Analyze document structure
        sentences = [sent.text.strip() for sent in doc.sents]
        
        # Additional scoring based on document structure
        if any("as a" in sent.lower() for sent in sentences):
            scores["User Story"] += 0.3
        
        if any(sent.strip().startswith(("Given", "When", "Then")) for sent in sentences):
            scores["User Story"] += 0.2
        
        if any(re.match(r"^\d+\.", sent.strip()) for sent in sentences):
            scores["Test Case"] += 0.2
        
        if "scope" in content.lower() and "objective" in content.lower():
            scores["BRD"] += 0.2
        
        if "system shall" in content.lower() or "must have" in content.lower():
            scores["FRD"] += 0.2
            
        return scores

    def get_document_type(self, content: str) -> Optional[str]:
        """
        Determine the most likely document type.
        Returns the document type with the highest confidence score if above threshold.
        """
        scores = self.identify_document_type(content)
        max_score = max(scores.values())
        max_type = max(scores.items(), key=lambda x: x[1])[0]
        
        # Require a minimum confidence threshold
        if max_score >= 0.3:
            return max_type
        return None