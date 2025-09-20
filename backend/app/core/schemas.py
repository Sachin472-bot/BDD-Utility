from typing import Optional, Dict, Any, List
from pydantic import BaseModel

class DocumentBase(BaseModel):
    content: str
    document_type: str  # BRD, FRD, User Story, Test Case
    format: str  # docx, pdf, txt

class FeatureFileResponse(BaseModel):
    feature_content: str
    suggested_steps: Dict[str, Any]
    document_type: str
    file_format: str

class DocumentAnalysisResponse(BaseModel):
    filename: str
    suggested_type: Optional[str]
    confidence_scores: Dict[str, float]
    file_format: Optional[str]

class StepDefinitionRequest(BaseModel):
    feature_content: str
    programming_language: str  # python, java, javascript, etc.
    framework: Optional[str] = None  # behave, cucumber, jest, etc.

class StepDefinitionResponse(BaseModel):
    step_definitions: Dict[str, str]  # step pattern -> implementation
    imports: list[str]  # required imports
    setup_code: Optional[str] = None  # any necessary setup code