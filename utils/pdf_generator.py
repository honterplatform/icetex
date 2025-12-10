"""
PDF generator utility for creating PDFs from Excel search results.
"""

from io import BytesIO
from typing import Dict, Any, List
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.enums import TA_LEFT


class PDFGenerator:
    """Utility class for generating PDFs from search results."""
    
    def __init__(self):
        """Initialize the PDF generator."""
        pass
    
    def generate_result_pdf(self, results: List[Dict[str, Any]], query: str) -> BytesIO:
        """
        Generate a PDF document from search results.
        
        Args:
            results: List of dictionaries containing search result data
            query: The search query that generated these results
            
        Returns:
            BytesIO buffer containing the PDF data
        """
        buffer = BytesIO()
        
        # Create PDF document (using A4 size which is similar to letter)
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=72)
        
        # Container for the 'Flowable' objects
        story = []
        
        # Add ICETEX logo at the top - left aligned
        logo_path = Path(__file__).parent.parent / "static" / "images" / "icetex.png"
        if logo_path.exists():
            try:
                logo = Image(str(logo_path), width=2*inch, height=0.6*inch)
                logo.hAlign = 'LEFT'
                story.append(logo)
                story.append(Spacer(1, 0.3*inch))
            except Exception:
                # If image fails to load, continue without logo
                pass
        
        # Define styles - using Helvetica (similar to Satoshi) since it's built-in to ReportLab
        # For true Satoshi font, you would need to download TTF files and register them
        styles = getSampleStyleSheet()
        
        # Title style - left aligned
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#111827'),
            spaceAfter=20,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        )
        
        # Header style - left aligned
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#111827'),
            spaceAfter=10,
            spaceBefore=20,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        )
        
        # Label style - left aligned, bold
        label_style = ParagraphStyle(
            'CustomLabel',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#6b7280'),
            spaceAfter=4,
            spaceBefore=0,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        )
        
        # Value style - left aligned, regular weight
        value_style = ParagraphStyle(
            'CustomValue',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#111827'),
            spaceAfter=16,
            leftIndent=0,
            alignment=TA_LEFT,
            fontName='Helvetica'
        )
        
        # Add title - left aligned
        title = Paragraph("ICETEX - Información de Contratista", title_style)
        story.append(title)
        story.append(Spacer(1, 0.25*inch))
        
        # Add search query info - left aligned
        query_style = ParagraphStyle(
            'QueryStyle',
            parent=styles['Normal'],
            fontSize=11,
            alignment=TA_LEFT,
            fontName='Helvetica',
            textColor=colors.HexColor('#111827'),
            spaceAfter=6
        )
        query_text = Paragraph(f"<b>Búsqueda realizada:</b> {self._escape_html(query)}", query_style)
        story.append(query_text)
        
        results_count = Paragraph(f"<b>Resultados encontrados:</b> {len(results)}", query_style)
        story.append(results_count)
        story.append(Spacer(1, 0.3*inch))
        
        # Process each result
        for idx, result in enumerate(results, 1):
            # Add result header
            main_title = result.get('CONTRATISTA : NOMBRE COMPLETO O RAZON SOCIAL', 
                                   result.get('No. \\nCto', f'Resultado {idx}'))
            
            header = Paragraph(f"Resultado {idx}: {self._escape_html(str(main_title))}", header_style)
            story.append(header)
            
            # Get ID if available
            subtitle = result.get('CONTRATISTA: NÚMERO DE IDENTIFICACIÓN', 
                                result.get('No. \\nCto', ''))
            if subtitle:
                id_style = ParagraphStyle(
                    'IdStyle',
                    parent=styles['Normal'],
                    fontSize=11,
                    alignment=TA_LEFT,
                    fontName='Helvetica',
                    textColor=colors.HexColor('#111827'),
                    spaceAfter=12
                )
                id_text = Paragraph(f"<b>ID:</b> {self._escape_html(str(subtitle))}", id_style)
                story.append(id_text)
            
            # Add spacing before fields
            story.append(Spacer(1, 0.15*inch))
            
            # Get all non-empty fields
            fields = []
            for key, value in result.items():
                # Skip empty values
                if value is None or str(value).strip().lower() in ['', 'nan', 'n/a', 'na']:
                    continue
                
                # Format key (replace underscores, capitalize)
                formatted_key = str(key).replace('_', ' ').title()
                
                # Format value
                formatted_value = str(value).strip()
                
                fields.append((formatted_key, formatted_value))
            
            # Display fields in organized list format (no table)
            if fields:
                for key, value in fields:
                    # Add label (bold, gray)
                    label = Paragraph(f"<b>{self._escape_html(key)}</b>", label_style)
                    story.append(label)
                    
                    # Add value (regular, black) - will wrap automatically
                    value_para = Paragraph(self._escape_html(str(value)), value_style)
                    story.append(value_para)
            
            # Add page break between results (except for the last one)
            if idx < len(results):
                story.append(PageBreak())
        
        # Build PDF
        doc.build(story)
        
        # Reset buffer position
        buffer.seek(0)
        return buffer
    
    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters for safe display in PDF."""
        if not text:
            return ""
        text = str(text)
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&#39;')
        return text
