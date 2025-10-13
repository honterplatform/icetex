"""
Knowledge Base system for ICETEX dependencies reference document.
Stores and processes the official ICETEX dependencies PDF for improved classification.
"""

import os
import json
import hashlib
from typing import Optional, Dict, Any
from datetime import datetime
from pathlib import Path

from .pdf_extractor import PDFExtractor


class ICETEXKnowledgeBase:
    """Manages the ICETEX dependencies reference document for enhanced classification."""
    
    def __init__(self, storage_dir: str = "knowledge_base"):
        """
        Initialize the knowledge base.
        
        Args:
            storage_dir: Directory to store knowledge base files
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        
        self.dependencies_file = self.storage_dir / "dependencies_info.json"
        self.reference_text_file = self.storage_dir / "reference_text.txt"
        self.pdf_extractor = PDFExtractor()
        
        # Load existing knowledge base
        self._load_knowledge_base()
    
    def _load_knowledge_base(self):
        """Load existing knowledge base data."""
        self.dependencies_info = {}
        self.reference_text = ""
        
        if self.dependencies_file.exists():
            try:
                with open(self.dependencies_file, 'r', encoding='utf-8') as f:
                    self.dependencies_info = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load dependencies info: {e}")
        
        if self.reference_text_file.exists():
            try:
                with open(self.reference_text_file, 'r', encoding='utf-8') as f:
                    self.reference_text = f.read()
            except Exception as e:
                print(f"Warning: Could not load reference text: {e}")
    
    def _save_knowledge_base(self):
        """Save knowledge base data to files."""
        try:
            # Save dependencies info
            with open(self.dependencies_file, 'w', encoding='utf-8') as f:
                json.dump(self.dependencies_info, f, indent=2, ensure_ascii=False)
            
            # Save reference text
            with open(self.reference_text_file, 'w', encoding='utf-8') as f:
                f.write(self.reference_text)
                
        except Exception as e:
            print(f"Error saving knowledge base: {e}")
    
    def upload_dependencies_pdf(self, pdf_path: str, description: str = "") -> Dict[str, Any]:
        """
        Upload and process the ICETEX dependencies PDF document.
        
        Args:
            pdf_path: Path to the PDF file
            description: Optional description of the document
            
        Returns:
            Dictionary with upload results
        """
        try:
            # Calculate file hash for change detection
            with open(pdf_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            
            # Check if this is the same file we already have
            if (self.dependencies_info.get('file_hash') == file_hash and 
                self.reference_text):
                return {
                    "success": True,
                    "message": "Document already uploaded and processed",
                    "file_hash": file_hash,
                    "text_length": len(self.reference_text)
                }
            
            # Extract text from PDF
            print(f"Processing dependencies PDF: {pdf_path}")
            extracted_text = self.pdf_extractor.extract_text(pdf_path)
            
            if not extracted_text or len(extracted_text.strip()) < 100:
                return {
                    "success": False,
                    "error": "Could not extract sufficient text from the PDF"
                }
            
            # Update knowledge base
            self.reference_text = extracted_text
            self.dependencies_info = {
                "file_hash": file_hash,
                "filename": os.path.basename(pdf_path),
                "upload_date": datetime.now().isoformat(),
                "description": description,
                "text_length": len(extracted_text),
                "last_processed": datetime.now().isoformat()
            }
            
            # Save to files
            self._save_knowledge_base()
            
            return {
                "success": True,
                "message": "Dependencies document uploaded and processed successfully",
                "file_hash": file_hash,
                "text_length": len(extracted_text),
                "filename": os.path.basename(pdf_path)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error processing PDF: {str(e)}"
            }
    
    def upload_dependencies_from_bytes(self, pdf_bytes: bytes, filename: str, description: str = "") -> Dict[str, Any]:
        """
        Upload and process dependencies PDF from bytes (for uploaded files).
        
        Args:
            pdf_bytes: PDF file content as bytes
            filename: Original filename
            description: Optional description
            
        Returns:
            Dictionary with upload results
        """
        try:
            # Calculate file hash
            file_hash = hashlib.md5(pdf_bytes).hexdigest()
            
            # Check if this is the same file we already have
            if (self.dependencies_info.get('file_hash') == file_hash and 
                self.reference_text):
                return {
                    "success": True,
                    "message": "Document already uploaded and processed",
                    "file_hash": file_hash,
                    "text_length": len(self.reference_text)
                }
            
            # Extract text from PDF bytes
            print(f"Processing dependencies PDF: {filename}")
            extracted_text = self.pdf_extractor.extract_from_bytes(pdf_bytes)
            
            if not extracted_text or len(extracted_text.strip()) < 100:
                return {
                    "success": False,
                    "error": "Could not extract sufficient text from the PDF"
                }
            
            # Update knowledge base
            self.reference_text = extracted_text
            self.dependencies_info = {
                "file_hash": file_hash,
                "filename": filename,
                "upload_date": datetime.now().isoformat(),
                "description": description,
                "text_length": len(extracted_text),
                "last_processed": datetime.now().isoformat()
            }
            
            # Save to files
            self._save_knowledge_base()
            
            return {
                "success": True,
                "message": "Dependencies document uploaded and processed successfully",
                "file_hash": file_hash,
                "text_length": len(extracted_text),
                "filename": filename
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error processing PDF: {str(e)}"
            }
    
    def get_reference_context(self, max_length: int = 8000) -> str:
        """
        Get the reference text to include in classification context.
        
        Args:
            max_length: Maximum length of context to return
            
        Returns:
            Reference text for use in classification
        """
        if not self.reference_text:
            return ""
        
        # If text is too long, truncate intelligently
        if len(self.reference_text) > max_length:
            # Try to find a good truncation point
            truncated = self.reference_text[:max_length]
            last_period = truncated.rfind('.')
            if last_period > max_length * 0.8:  # If we can find a period in the last 20%
                return truncated[:last_period + 1]
            else:
                return truncated + "..."
        
        return self.reference_text
    
    def get_knowledge_base_info(self) -> Dict[str, Any]:
        """Get information about the current knowledge base."""
        return {
            "has_reference_document": bool(self.reference_text),
            "reference_text_length": len(self.reference_text) if self.reference_text else 0,
            "dependencies_info": self.dependencies_info,
            "last_updated": self.dependencies_info.get('upload_date', 'Never')
        }
    
    def clear_knowledge_base(self) -> Dict[str, Any]:
        """Clear the knowledge base."""
        try:
            # Remove files
            if self.dependencies_file.exists():
                self.dependencies_file.unlink()
            if self.reference_text_file.exists():
                self.reference_text_file.unlink()
            
            # Clear memory
            self.dependencies_info = {}
            self.reference_text = ""
            
            return {
                "success": True,
                "message": "Knowledge base cleared successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error clearing knowledge base: {str(e)}"
            }
    
    def is_available(self) -> bool:
        """Check if the knowledge base has reference material."""
        return bool(self.reference_text and len(self.reference_text.strip()) > 100)
