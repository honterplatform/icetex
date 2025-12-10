"""
PDF generator utility for creating PDFs from Excel search results.
"""

from io import BytesIO
from typing import Dict, Any, List
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


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
        
        # Define styles
        styles = getSampleStyleSheet()
        
        # Title style
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#111827'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Header style
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#111827'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        )
        
        # Label style
        label_style = ParagraphStyle(
            'CustomLabel',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#6b7280'),
            spaceAfter=4,
            fontName='Helvetica-Bold'
        )
        
        # Value style
        value_style = ParagraphStyle(
            'CustomValue',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#111827'),
            spaceAfter=12,
            leftIndent=20
        )
        
        # Add title
        title = Paragraph("ICETEX - Información de Contratista", title_style)
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        # Add search query info
        query_text = Paragraph(f"<b>Búsqueda realizada:</b> {self._escape_html(query)}", styles['Normal'])
        story.append(query_text)
        story.append(Spacer(1, 0.1*inch))
        
        results_count = Paragraph(f"<b>Resultados encontrados:</b> {len(results)}", styles['Normal'])
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
                id_text = Paragraph(f"<b>ID:</b> {self._escape_html(str(subtitle))}", styles['Normal'])
                story.append(id_text)
                story.append(Spacer(1, 0.1*inch))
            
            # Add divider line
            story.append(Spacer(1, 0.05*inch))
            
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
            
            # Create table for fields
            if fields:
                # Create data for table
                table_data = []
                for key, value in fields:
                    # ReportLab's Paragraph will handle text wrapping automatically
                    # We just need to escape HTML and let it wrap naturally
                    table_data.append([
                        Paragraph(f"<b>{self._escape_html(key)}</b>", label_style),
                        Paragraph(self._escape_html(str(value)), value_style)
                    ])
                
                # Create table
                table = Table(table_data, colWidths=[2.5*inch, 4.5*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f9fafb')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('LEFTPADDING', (0, 0), (0, -1), 12),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ]))
                
                story.append(table)
            
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
