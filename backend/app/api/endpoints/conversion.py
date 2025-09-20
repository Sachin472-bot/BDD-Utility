from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import List, Dict, Any, Optional
import PyPDF2
from docx import Document
from io import BytesIO
from ...services.document_parser import DocumentParser
from ...services.gherkin_generator import GherkinGenerator
from ...services.document_type_identifier import DocumentTypeIdentifier
from ...core.schemas import FeatureFileResponse, DocumentAnalysisResponse

# Create two separate routers
router = APIRouter()  # for new endpoints
legacy_router = APIRouter()  # for legacy endpoints
document_parser = DocumentParser()
gherkin_generator = GherkinGenerator()
doc_identifier = DocumentTypeIdentifier()

@router.post("/analyze", response_model=DocumentAnalysisResponse)
async def analyze_document(
    file: UploadFile = File(description="The document file to analyze (PDF, DOCX, or TXT)")
):
    """
    Analyze document content and suggest document type
    """
    try:
        content = await file.read()
        text_content = await extract_text_from_file(content, file.filename)
        
        # Analyze document type
        doc_scores = doc_identifier.identify_document_type(text_content)
        suggested_type = doc_identifier.get_document_type(text_content)
        
        return {
            "filename": file.filename,
            "suggested_type": suggested_type,
            "confidence_scores": doc_scores,
            "file_format": file.filename.split('.')[-1].lower() if '.' in file.filename else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Enhanced conversion endpoint
@legacy_router.post("/convert-to-feature", response_model=FeatureFileResponse)
async def convert_to_feature(
    file: UploadFile = File(description="The document file to convert (PDF, DOCX, or TXT)"),
    doc_type: Optional[str] = Form(None, description="Document type (optional, will be auto-detected if not provided)")
):
    """
    Enhanced endpoint for converting document to feature file with auto-detection
    """
    # Validate file is provided
    if not file:
        raise HTTPException(
            status_code=400,
            detail="No file uploaded. Please provide a document file."
        )

    # Validate document type
    valid_doc_types = ["BRD", "FRD", "User Story", "Test Case"]
    if not doc_type:
        raise HTTPException(
            status_code=400,
            detail=f"Document type is required. Valid types are: {', '.join(valid_doc_types)}"
        )
    
    if doc_type not in valid_doc_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid document type. Valid types are: {', '.join(valid_doc_types)}"
        )

    try:
        # Validate file format
        file_ext = file.filename.lower().split('.')[-1] if '.' in file.filename else ''
        valid_formats = {'pdf', 'docx', 'txt'}
        
        if file_ext not in valid_formats:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format: .{file_ext}. Please upload one of: {', '.join(valid_formats)}"
            )

        # Read file content
        try:
            content = await file.read()
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error reading file: {str(e)}"
            )
        
        # Extract text based on file type
        if file_ext == 'pdf':
            text_content = await extract_text_from_pdf(content)
        elif file_ext == 'docx':
            text_content = await extract_text_from_docx(content)
        elif file_ext == 'txt':
            try:
                text_content = content.decode('utf-8')
            except UnicodeDecodeError:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid text file encoding. Please ensure the file is UTF-8 encoded."
                )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format: .{file_ext}. Please upload PDF, DOCX, or TXT files."
            )

        # Parse document content
        parsed_content = document_parser.parse_document(text_content, doc_type)
        
        # Generate feature file
        feature_content = gherkin_generator.generate_feature(
            parsed_content,
            feature_name=file.filename.rsplit('.', 1)[0],
            doc_type=doc_type
        )

        return {
            "feature_content": feature_content,
            "suggested_steps": parsed_content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def extract_text_from_file(content: bytes, filename: str) -> str:
    """Extract text content from file based on its format"""
    try:
        file_ext = filename.lower().split('.')[-1] if '.' in filename else ''
        
        if file_ext == 'pdf':
            pdf_file = BytesIO(content)
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
            
        elif file_ext == 'docx':
            doc = Document(BytesIO(content))
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
            
        elif file_ext == 'txt':
            try:
                return content.decode('utf-8')
            except UnicodeDecodeError:
                return content.decode('latin-1')  # fallback encoding
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format: .{file_ext}"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error processing {filename}: {str(e)}"
        )

@router.post("/convert")
async def convert_document(
    files: List[UploadFile] = File(...),
    doc_type: str = None
):
    """
    Convert uploaded documents to Gherkin feature files
    Supported formats: PDF, DOCX, TXT
    Document types: BRD, FRD, User Story, Test Case
    """
    if not doc_type:
        raise HTTPException(status_code=400, detail="Document type must be specified")
    
    if doc_type not in ["BRD", "FRD", "User Story", "Test Case"]:
        raise HTTPException(status_code=400, detail="Unsupported document type")

    results = []
    for file in files:
        try:
            content = await file.read()
            
            # Extract text based on file type
            if file.filename.lower().endswith('.pdf'):
                text_content = await extract_text_from_pdf(content)
            elif file.filename.lower().endswith('.docx'):
                text_content = await extract_text_from_docx(content)
            elif file.filename.lower().endswith('.txt'):
                text_content = content.decode('utf-8')
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Unsupported file format. Please upload PDF, DOCX, or TXT files."
                )

            # Parse document content
            parsed_content = document_parser.parse_document(text_content, doc_type)
            
            # Generate Gherkin feature file
            feature_content = gherkin_generator.generate_feature(
                parsed_content,
                feature_name=file.filename.rsplit('.', 1)[0],
                doc_type=doc_type
            )

            results.append({
                "filename": file.filename,
                "feature_content": feature_content,
                "parsed_content": parsed_content
            })

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing {file.filename}: {str(e)}")

    return {
        "status": "success",
        "results": results
    }

@router.post("/validate")
async def validate_document(
    file: UploadFile = File(...),
    doc_type: str = None
):
    """
    Validate document structure and content before conversion
    Returns parsed structure without generating feature files
    """
    if not doc_type:
        raise HTTPException(status_code=400, detail="Document type must be specified")

    try:
        content = await file.read()
        
        # Extract text based on file type
        if file.filename.lower().endswith('.pdf'):
            text_content = await extract_text_from_pdf(content)
        elif file.filename.lower().endswith('.docx'):
            text_content = await extract_text_from_docx(content)
        elif file.filename.lower().endswith('.txt'):
            text_content = content.decode('utf-8')
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format. Please upload PDF, DOCX, or TXT files."
            )

        # Parse document content
        parsed_content = document_parser.parse_document(text_content, doc_type)
        
        return {
            "status": "success",
            "filename": file.filename,
            "parsed_structure": parsed_content
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating document: {str(e)}")