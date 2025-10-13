"""
FastAPI application for ICETEX petition classification.
Receives PDF petitions, extracts text, and classifies them using OpenAI API.
"""

import os
import tempfile
from typing import Optional
from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from utils.pdf_extractor import PDFExtractor
from utils.openai_classifier import ICETEXClassifier
from utils.knowledge_base import ICETEXKnowledgeBase

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="ICETEX Petition Classifier",
    description="AI system for classifying ICETEX petitions to appropriate dependencies",
    version="1.0.0"
)

# Setup templates
templates = Jinja2Templates(directory="templates")

# Mount static files directory for images, CSS, JS, etc.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize extractors, classifiers, and knowledge base
pdf_extractor = PDFExtractor()
knowledge_base = ICETEXKnowledgeBase()
openai_classifier = None  # Will be initialized when API key is available


def get_classifier() -> ICETEXClassifier:
    """Get or initialize the OpenAI classifier."""
    global openai_classifier
    if openai_classifier is None:
        try:
            openai_classifier = ICETEXClassifier(knowledge_base=knowledge_base)
        except ValueError as e:
            raise HTTPException(
                status_code=500,
                detail=f"OpenAI API key not configured. Please set OPENAI_API_KEY in .env file. Error: {str(e)}"
            )
    return openai_classifier


@app.get("/", response_class=HTMLResponse)
async def upload_form(request: Request):
    """
    Display the upload form for PDF petitions.
    """
    return templates.TemplateResponse("upload.html", {"request": request})


@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    """
    Display the admin panel for managing the knowledge base.
    """
    return templates.TemplateResponse("admin.html", {"request": request})


@app.post("/classify")
async def classify_petition(file: UploadFile = File(...)):
    """
    Classify an uploaded PDF petition.
    
    Process:
    1. Validate the uploaded file is a PDF
    2. Extract text from the PDF
    3. Send text to OpenAI API for classification
    4. Return classification results
    
    Returns:
        JSON response with:
        - dependencia: ICETEX office that should handle the petition
        - confianza: Confidence level (percentage)
        - motivo: Explanation for the classification
        - palabras_clave: Keywords detected in the text
    """
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted. Please upload a PDF document."
        )
    
    try:
        # Read file contents
        file_contents = await file.read()
        
        if len(file_contents) == 0:
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty."
            )
        
        # Extract text from PDF
        print(f"Processing file: {file.filename} ({len(file_contents)} bytes)")
        extracted_text = pdf_extractor.extract_from_bytes(file_contents)
        
        if not extracted_text or len(extracted_text.strip()) < 10:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Could not extract sufficient text from the PDF",
                    "detail": "The PDF might be corrupted, password-protected, or contain no readable text. Please ensure the document is a valid PDF with text content.",
                    "extracted_text": extracted_text[:500] if extracted_text else ""
                }
            )
        
        print(f"Extracted {len(extracted_text)} characters from PDF")
        
        # Classify using OpenAI
        classifier = get_classifier()
        classification_result = classifier.classify_with_metadata(extracted_text)
        
        # Add filename to response
        classification_result["filename"] = file.filename
        
        return JSONResponse(content=classification_result)
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing petition: {str(e)}"
        )


@app.get("/result", response_class=HTMLResponse)
async def result_page(request: Request):
    """
    Display the results page (used after classification).
    """
    return templates.TemplateResponse("result.html", {"request": request})


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    api_key_configured = os.getenv("OPENAI_API_KEY") is not None
    
    return {
        "status": "healthy",
        "openai_configured": api_key_configured,
        "model": os.getenv("OPENAI_MODEL", "gpt-4-turbo")
    }


@app.get("/dependencies")
async def list_dependencies():
    """
    Return the list of ICETEX dependencies that can be assigned.
    """
    dependencies = [
        {
            "name": "Oficina Asesora Jurídica",
            "description": "Legal interpretation, contracts, administrative law, litigation, disciplinary processes"
        },
        {
            "name": "Oficina Asesora de Planeación",
            "description": "Strategic planning, institutional performance, indicators, process optimization"
        },
        {
            "name": "Oficina Asesora de Comunicaciones",
            "description": "Institutional communications, public relations, press releases, brand reputation"
        },
        {
            "name": "Oficina de Riesgos",
            "description": "Risk management, operational risk, compliance with internal control systems"
        },
        {
            "name": "Oficina de Control Interno",
            "description": "Audits, internal oversight, compliance, anti-corruption plans"
        },
        {
            "name": "Oficina de Relaciones Internacionales",
            "description": "International scholarships, cooperation programs, partnerships abroad"
        },
        {
            "name": "Oficina Comercial y de Mercadeo",
            "description": "Promotion of products, user acquisition, advertising, customer service"
        },
        {
            "name": "Vicepresidencia de Crédito y Cobranza",
            "description": "Credit granting, collection, loan management, payment agreements"
        },
        {
            "name": "Vicepresidencia de Operaciones y Tecnología",
            "description": "Systems management, IT infrastructure, platform maintenance"
        },
        {
            "name": "Vicepresidencia Financiera",
            "description": "Treasury, accounting, financial management, budget control"
        },
        {
            "name": "Vicepresidencia de Fondos en Administración",
            "description": "Management of special education funds, forgiveness (condonación) processes, verification of fund regulations"
        },
        {
            "name": "Secretaría General",
            "description": "Contractual management, records, administrative coordination, HR, disciplinary support"
        }
    ]
    
    return {"dependencies": dependencies}


@app.post("/upload-dependencies")
async def upload_dependencies_document(file: UploadFile = File(...)):
    """
    Upload the official ICETEX dependencies PDF document for enhanced classification.
    
    This endpoint allows you to upload the official ICETEX document that contains
    detailed information about each dependency's responsibilities. This will be
    used to improve classification accuracy.
    
    Args:
        file: PDF file containing ICETEX dependencies information
        
    Returns:
        JSON response with upload results
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted for dependencies document."
        )
    
    try:
        # Read file contents
        file_contents = await file.read()
        
        if len(file_contents) == 0:
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty."
            )
        
        # Upload to knowledge base
        result = knowledge_base.upload_dependencies_from_bytes(
            file_contents, 
            file.filename,
            "Official ICETEX Dependencies Document"
        )
        
        if result["success"]:
            # Reset classifier to use new knowledge base
            global openai_classifier
            openai_classifier = None
            
            return JSONResponse(content={
                "success": True,
                "message": result["message"],
                "filename": result.get("filename"),
                "text_length": result.get("text_length"),
                "knowledge_base_info": knowledge_base.get_knowledge_base_info()
            })
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to process dependencies document: {result['error']}"
            )
            
    except Exception as e:
        print(f"Error uploading dependencies document: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading dependencies document: {str(e)}"
        )


@app.get("/knowledge-base")
async def get_knowledge_base_info():
    """
    Get information about the current knowledge base.
    
    Returns:
        JSON response with knowledge base status and information
    """
    try:
        info = knowledge_base.get_knowledge_base_info()
        return JSONResponse(content=info)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving knowledge base info: {str(e)}"
        )


@app.delete("/knowledge-base")
async def clear_knowledge_base():
    """
    Clear the knowledge base (remove uploaded dependencies document).
    
    Returns:
        JSON response with operation results
    """
    try:
        result = knowledge_base.clear_knowledge_base()
        
        if result["success"]:
            # Reset classifier
            global openai_classifier
            openai_classifier = None
            
            return JSONResponse(content=result)
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to clear knowledge base: {result['error']}"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error clearing knowledge base: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

