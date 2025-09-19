from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Optional
from ...core.schemas import DocumentBase, FeatureFileResponse, StepDefinitionRequest, StepDefinitionResponse
from ...services.document_parser import DocumentParser
from ...services.gherkin_generator import GherkinGenerator
from ...services.step_definition_generator import StepDefinitionGenerator

router = APIRouter()
document_parser = DocumentParser()
gherkin_generator = GherkinGenerator()
step_generator = StepDefinitionGenerator()

@router.post("/convert-to-feature", response_model=FeatureFileResponse)
async def convert_to_feature(file: UploadFile = File(...), doc_type: str = None):
    """
    Convert uploaded document to Gherkin feature file
    """
    if not doc_type:
        raise HTTPException(status_code=400, detail="Document type is required")

    try:
        # Read file content
        content = await file.read()
        
        if file.filename.endswith('.docx'):
            # Handle docx files
            from docx import Document
            from io import BytesIO
            doc = Document(BytesIO(content))
            text_content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        else:
            # Handle plain text files
            text_content = content.decode()

        # Parse document
        parsed_data = document_parser.parse_document(text_content, doc_type)
        
        # Generate feature file
        feature_content = gherkin_generator.generate_feature(parsed_data, doc_type)
        
        return {
            "feature_content": feature_content,
            "suggested_steps": parsed_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-steps", response_model=StepDefinitionResponse)
async def generate_steps(request: StepDefinitionRequest):
    """
    Generate step definitions from feature file content
    """
    try:
        result = step_generator.generate_step_definitions(
            request.feature_content,
            request.programming_language,
            request.framework
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))