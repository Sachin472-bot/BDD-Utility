from fastapi import APIRouter, UploadFile, File, HTTPException
from ..core.schemas import DocumentBase, FeatureFileResponse, StepDefinitionRequest, StepDefinitionResponse
from ..services.document_parser import DocumentParser
from ..services.gherkin_generator import GherkinGenerator
from ..services.step_definition_generator import StepDefinitionGenerator
import docx
import io

router = APIRouter()
document_parser = DocumentParser()
gherkin_generator = GherkinGenerator()
step_generator = StepDefinitionGenerator()

@router.post("/convert-to-feature", response_model=FeatureFileResponse)
async def convert_to_feature(file: UploadFile = File(...), doc_type: str = None):
    """Convert uploaded document to Gherkin feature file."""
    if not doc_type:
        raise HTTPException(status_code=400, detail="Document type is required")

    try:
        content = await _read_file_content(file)
        parsed_data = document_parser.parse_document(content, doc_type)
        feature_content = gherkin_generator.generate_feature(parsed_data, doc_type)
        
        return FeatureFileResponse(
            feature_content=feature_content,
            suggested_steps={}  # TODO: Implement step suggestions
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-steps", response_model=StepDefinitionResponse)
async def generate_steps(request: StepDefinitionRequest):
    """Generate step definitions from feature file content."""
    try:
        result = step_generator.generate_step_definitions(
            request.feature_content,
            request.programming_language,
            request.framework
        )
        
        return StepDefinitionResponse(
            step_definitions=result["step_definitions"],
            imports=result["imports"],
            setup_code=result.get("setup_code")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def _read_file_content(file: UploadFile) -> str:
    """Read content from uploaded file."""
    content_bytes = await file.read()
    
    if file.filename.endswith('.docx'):
        doc = docx.Document(io.BytesIO(content_bytes))
        return "\n".join(paragraph.text for paragraph in doc.paragraphs)
    else:
        return content_bytes.decode()