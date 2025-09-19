from typing import Optional, Dict, Any
from pydantic import BaseModel

class DocumentBase(BaseModel):
    content: str
    document_type: str  # BRD, FRD, User Story, Test Case
    format: str  # docx, pdf, txt

class FeatureFileResponse(BaseModel):
    feature_content: str
    suggested_steps: Dict[str, Any]

class StepDefinitionRequest(BaseModel):
    feature_content: str
    programming_language: str  # python, java, javascript, etc.
    framework: Optional[str] = None  # behave, cucumber, jest, etc.

class StepDefinitionResponse(BaseModel):
    step_definitions: Dict[str, str]  # step pattern -> implementation
    imports: list[str]  # required imports
    setup_code: Optional[str] = None  # any necessary setup code