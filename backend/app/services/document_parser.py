import spacy
from typing import Dict, Any, List
import re
from pathlib import Path
import json

class DocumentParser:
    def __init__(self):
        # Load English language model with NLP pipeline
        self.nlp = spacy.load("en_core_web_sm")
        
        # Load custom keyword patterns for different document types
        self.patterns = self._load_patterns()

    def _load_patterns(self) -> Dict[str, Dict[str, List[str]]]:
        """Load custom patterns for different document types"""
        return {
            "BRD": {
                "requirements": [
                    r"must\s+(?:be able to|have|provide|support|allow)",
                    r"should\s+(?:be able to|have|provide|support|allow)",
                    r"needs? to",
                    r"will\s+(?:be able to|have|provide|support|allow)"
                ],
                "actors": [
                    r"(?:the\s+)?(?:user|system|admin|customer|client)",
                    r"(?:the\s+)?(?:application|platform|service)",
                ],
                "scenarios": [
                    r"when.*then",
                    r"if.*then",
                    r"given.*when.*then"
                ]
            },
            "User Story": {
                "patterns": [
                    r"As (?:an?|the)\s+(.+?)\s+I want to\s+(.+?)\s+so that\s+(.+)",
                    r"As (?:an?|the)\s+(.+?)\s+I need to\s+(.+?)\s+so that\s+(.+)",
                    r"As (?:an?|the)\s+(.+?)\s+I should be able to\s+(.+?)\s+so that\s+(.+)"
                ]
            },
            "Test Case": {
                "preconditions": [
                    r"(?:Pre-conditions?|Prerequisites?|Given):?\s*(.*)",
                    r"Before\s+(?:the test|testing)\s*(.*)"
                ],
                "steps": [
                    r"(?:Step|Action)\s*\d+:?\s*(.*)",
                    r"^\d+\.\s*(.*)",
                    r"When\s+(.*)"
                ],
                "expected_results": [
                    r"(?:Expected|Expected Result|Then):?\s*(.*)",
                    r"(?:Verify|Validate):?\s*(.*)",
                    r"Should\s+(.*)"
                ]
            }
        }

    def parse_document(self, content: str, doc_type: str) -> Dict[str, Any]:
        """Parse document content based on its type using NLP"""
        if doc_type == "BRD" or doc_type == "FRD":
            return self._parse_requirements_doc(content)
        elif doc_type == "User Story":
            return self._parse_user_story(content)
        elif doc_type == "Test Case":
            return self._parse_test_case(content)
        else:
            raise ValueError(f"Unsupported document type: {doc_type}")

    def _parse_requirements_doc(self, content: str) -> Dict[str, Any]:
        """Parse BRD/FRD documents using NLP"""
        doc = self.nlp(content)
        
        # Extract requirements
        requirements = []
        actors = set()
        scenarios = []
        
        # Process each sentence
        for sent in doc.sents:
            sent_text = sent.text.strip()
            
            # Extract requirements
            for pattern in self.patterns["BRD"]["requirements"]:
                if re.search(pattern, sent_text, re.IGNORECASE):
                    requirements.append(sent_text)
                    
                    # Extract actors from requirements
                    for actor_pattern in self.patterns["BRD"]["actors"]:
                        actor_matches = re.findall(actor_pattern, sent_text, re.IGNORECASE)
                        actors.update(actor_matches)
                    
                    break
            
            # Extract scenarios
            for pattern in self.patterns["BRD"]["scenarios"]:
                if re.search(pattern, sent_text, re.IGNORECASE):
                    scenarios.append(sent_text)
                    break

        return {
            "requirements": requirements,
            "actors": list(actors),
            "scenarios": scenarios
        }

    def _parse_user_story(self, content: str) -> Dict[str, Any]:
        """Parse user stories using NLP"""
        stories = []
        
        # Split content into lines and process each line
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # Try to match user story patterns
            for pattern in self.patterns["User Story"]["patterns"]:
                matches = re.match(pattern, line, re.IGNORECASE)
                if matches:
                    role, want, benefit = matches.groups()
                    stories.append({
                        "role": role.strip(),
                        "want": want.strip(),
                        "benefit": benefit.strip(),
                        "acceptance_criteria": self._extract_acceptance_criteria(content)
                    })
                    break
        
        return {"stories": stories}

    def _parse_test_case(self, content: str) -> Dict[str, Any]:
        """Parse test cases using NLP"""
        doc = self.nlp(content)
        
        preconditions = []
        steps = []
        expected_results = []
        
        current_section = None
        
        # Process each line
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Check for section headers
            if any(re.match(pattern, line, re.IGNORECASE) for pattern in self.patterns["Test Case"]["preconditions"]):
                current_section = "preconditions"
                continue
            elif any(re.match(pattern, line, re.IGNORECASE) for pattern in self.patterns["Test Case"]["steps"]):
                current_section = "steps"
            elif any(re.match(pattern, line, re.IGNORECASE) for pattern in self.patterns["Test Case"]["expected_results"]):
                current_section = "expected_results"
            
            # Clean up the line by removing common prefixes
            clean_line = re.sub(r"^(?:Step|Action)\s*\d+:?\s*", "", line)
            clean_line = re.sub(r"^\d+\.\s*", "", clean_line)
            
            # Add line to appropriate section
            if current_section == "preconditions":
                preconditions.append(clean_line)
            elif current_section == "steps":
                steps.append(clean_line)
            elif current_section == "expected_results":
                expected_results.append(clean_line)
        
        return {
            "preconditions": preconditions,
            "steps": steps,
            "expected_results": expected_results
        }

    def _extract_acceptance_criteria(self, content: str) -> List[Dict[str, str]]:
        """Extract acceptance criteria from user story content"""
        criteria = []
        doc = self.nlp(content)
        
        # Look for common acceptance criteria patterns
        for sent in doc.sents:
            sent_text = sent.text.strip().lower()
            if any(keyword in sent_text for keyword in ["given", "when", "then", "verify", "check", "ensure"]):
                # Categorize the criterion
                if sent_text.startswith("given"):
                    criteria.append({"type": "given", "text": sent.text})
                elif sent_text.startswith("when"):
                    criteria.append({"type": "when", "text": sent.text})
                elif sent_text.startswith("then"):
                    criteria.append({"type": "then", "text": sent.text})
                else:
                    criteria.append({"type": "verification", "text": sent.text})
        
        return criteria