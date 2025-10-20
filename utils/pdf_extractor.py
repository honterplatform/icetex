"""
PDF text extraction module.
Handles both text-based PDFs (using pdfplumber) and scanned PDFs (using pytesseract + pdf2image).
"""

import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import io
import tempfile
import os
from typing import Optional


class PDFExtractor:
    """Extracts text from PDF files, handling both digital and scanned documents."""
    
    def __init__(self):
        # You can set custom tesseract path if needed
        # pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
        pass
    
    def extract_text(self, pdf_path: str) -> str:
        """
        Extract text from PDF file.
        First tries pdfplumber (fast, for text-based PDFs).
        If minimal text is found, falls back to OCR (for scanned PDFs).
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as string
        """
        # Try text-based extraction first
        text = self._extract_with_pdfplumber(pdf_path)
        
        # If we got very little text, it's probably a scanned PDF
        if len(text.strip()) < 100:
            print(f"Limited text found ({len(text)} chars). Attempting OCR...")
            try:
                ocr_text = self._extract_with_ocr(pdf_path)
                if len(ocr_text) > len(text):
                    text = ocr_text
            except Exception as e:
                print(f"OCR failed: {e}")
                # If OCR fails, return what we have and add a note
                if len(text.strip()) == 0:
                    text = "OCR no disponible. Este PDF parece ser una imagen escaneada. Por favor, use un PDF con texto extraíble o contacte al administrador para configurar OCR."
                else:
                    text += f"\n\n[Nota: OCR no disponible - {str(e)}]"
        
        return text.strip()
    
    def _extract_with_pdfplumber(self, pdf_path: str) -> str:
        """Extract text using pdfplumber (for text-based PDFs)."""
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            print(f"Extracted {len(text)} characters using pdfplumber")
        except Exception as e:
            print(f"Error extracting with pdfplumber: {e}")
        
        return text
    
    def _extract_with_ocr(self, pdf_path: str) -> str:
        """Extract text using OCR (for scanned PDFs)."""
        text = ""
        try:
            # Check if tesseract is available
            try:
                pytesseract.get_tesseract_version()
            except Exception:
                raise Exception("tesseract is not installed or it's not in your PATH. See README file for more information.")
            
            # Convert PDF to images
            images = convert_from_path(pdf_path, dpi=300)
            
            print(f"Processing {len(images)} pages with OCR...")
            
            # Perform OCR on each page
            for i, image in enumerate(images):
                print(f"OCR processing page {i+1}/{len(images)}...")
                page_text = pytesseract.image_to_string(image, lang='spa')
                text += page_text + "\n"
            
            print(f"Extracted {len(text)} characters using OCR")
        except Exception as e:
            print(f"Error extracting with OCR: {e}")
            # Provide more helpful error message
            if "tesseract" in str(e).lower():
                raise Exception(f"OCR extraction failed: {str(e)}. Make sure Tesseract and Poppler are installed.")
            else:
                raise Exception(f"OCR extraction failed: {str(e)}")
        
        return text
    
    def extract_from_bytes(self, pdf_bytes: bytes) -> str:
        """
        Extract text from PDF bytes (useful for uploaded files).
        
        Args:
            pdf_bytes: PDF file content as bytes
            
        Returns:
            Extracted text as string
        """
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_bytes)
            tmp_path = tmp_file.name
        
        try:
            text = self.extract_text(tmp_path)
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
        
        return text

