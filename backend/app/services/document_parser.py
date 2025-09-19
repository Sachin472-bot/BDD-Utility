import spacy
from typing import List, Dict, Any
import re

class DocumentParser:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    def parse_document(self, content: str, doc_type: str) -> Dict[str, Any]:
        """Parse document content based on its type."""
        if doc_type == "BRD":
            return self._parse_brd(content)
        elif doc_type == "FRD":
            return self._parse_frd(content)
        elif doc_type == "User Story":
            return self._parse_user_story(content)
        elif doc_type == "Test Case":
            return self._parse_test_case(content)
        else:
            raise ValueError(f"Unsupported document type: {doc_type}")

    def _parse_brd(self, content: str) -> Dict[str, Any]:
        # Extract business requirements and convert to scenarios
        doc = self.nlp(content)
        requirements = []
        
        # TODO: Implement BRD parsing logic
        # Look for requirement patterns, business rules, etc.
        
        return {"requirements": requirements}

    def _parse_user_story(self, content: str) -> Dict[str, Any]:
        # Parse user story in format: As a [role] I want [feature] so that [benefit]
        pattern = r"As (?:an?|the) (.+?) I want to? (.+?) so that (.+)"
        matches = re.findall(pattern, content, re.IGNORECASE)
        
        stories = []
        for role, want, benefit in matches:
            stories.append({
                "role": role.strip(),
                "want": want.strip(),
                "benefit": benefit.strip()
            })
        
        return {"stories": stories}

    def _parse_test_case(self, content: str) -> Dict[str, Any]:
        # Extract test steps, preconditions, and expected results
        sections = {
            "preconditions": [],
            "steps": [],
            "expected_results": []
        }
        
        # TODO: Implement test case parsing logic
        # Look for numbered steps, preconditions, expected results
        
        return sections