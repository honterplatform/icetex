"""
OpenAI API integration for ICETEX petition classification.
Uses GPT-4 to classify petitions into the appropriate ICETEX dependency.
"""

import os
import json
from typing import Dict, Any
from dotenv import load_dotenv

# Import OpenAI - force legacy API to avoid compatibility issues
import openai
OPENAI_NEW_API = False

# Load environment variables
load_dotenv()


class ICETEXClassifier:
    """Classifies ICETEX petitions using OpenAI API."""
    
    SYSTEM_PROMPT = """Eres un sistema de clasificación de IA para peticiones de ICETEX.  
Tu única función es leer el texto de una petición (en español) y decidir qué dependencia de ICETEX debe manejarla, basándote en el "Manual de Funciones y Competencias Laborales ICETEX V2".

### FORMATO DE SALIDA (siempre devolver JSON válido)
{
  "dependencia": "",
  "confianza": "",
  "motivo": "",
  "palabras_clave": []
}

### CONTEXTO Y REGLAS DE DECISIÓN
1. Si la petición menciona **fondos, convenios, condonación, becas, crédito condonable**, → elegir "Vicepresidencia de Fondos en Administración".
2. Si menciona **demanda, sanción, resolución, fallo, normatividad, derecho, apelación, abogado**, → "Oficina Asesora Jurídica".
3. Si menciona **riesgos, cumplimiento, control interno, auditoría, transparencia**, → "Oficina de Riesgos" o "Oficina de Control Interno" (según el enfoque).
4. Si menciona **planeación, estrategia, indicadores, metas institucionales**, → "Oficina Asesora de Planeación".
5. Si menciona **tecnología, plataforma, sistema, errores técnicos, mantenimiento**, → "Vicepresidencia de Operaciones y Tecnología".
6. Si menciona **comunicación, prensa, medios, campañas**, → "Oficina Asesora de Comunicaciones".
7. Si menciona **cobro, mora, pagos, deudas, cartera**, → "Vicepresidencia de Crédito y Cobranza".
8. Si menciona **presupuesto, finanzas, tesorería, contabilidad**, → "Vicepresidencia Financiera".
9. Si menciona **internacional, becas en el exterior, cooperación**, → "Oficina de Relaciones Internacionales".
10. Si menciona **comercial, mercadeo, usuarios, aliados estratégicos, atención al cliente**, → "Oficina Comercial y de Mercadeo".
11. Si menciona **personal, contratación, archivos, secretaría**, → "Secretaría General".
12. Si es ambiguo, selecciona la dependencia más probable y reduce la confianza en consecuencia.

### EJEMPLOS
Entrada: "Solicito la condonación del crédito educativo otorgado mediante el Fondo Bicentenario del Distrito de Cartagena."
Salida:
{
  "dependencia": "Vicepresidencia de Fondos en Administración",
  "confianza": "96%",
  "motivo": "La petición solicita la condonación de un crédito de un fondo administrado, el cual es manejado por la Vicepresidencia de Fondos en Administración.",
  "palabras_clave": ["condonación", "fondo", "crédito educativo"]
}

IMPORTANTE: TODAS las respuestas deben estar en español. El campo "motivo" debe explicar en español por qué se asignó esta dependencia."""
    
    def __init__(self, api_key: str = None, model: str = None, knowledge_base=None):
        """
        Initialize the classifier.
        
        Args:
            api_key: OpenAI API key (if None, reads from OPENAI_API_KEY env var)
            model: Model to use (default: gpt-4-turbo)
            knowledge_base: ICETEXKnowledgeBase instance for reference document
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Set OPENAI_API_KEY environment variable "
                "or pass it to the constructor."
            )
        
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4-turbo")
        self.knowledge_base = knowledge_base
        
        # Initialize OpenAI client - use legacy API only
        openai.api_key = self.api_key
        self.client = openai
        print("✅ OpenAI client initialized successfully (legacy API)")
    
    def classify(self, petition_text: str) -> Dict[str, Any]:
        """
        Classify a petition text into the appropriate ICETEX dependency.
        
        Args:
            petition_text: The extracted text from the petition PDF
            
        Returns:
            Dictionary with classification results:
            - dependencia: The ICETEX office that should handle it
            - confianza: Confidence level (percentage)
            - motivo: Explanation for the classification
            - palabras_clave: Keywords detected in the text
        """
        if not petition_text or len(petition_text.strip()) < 10:
            return {
                "dependencia": "Error",
                "confianza": "0%",
                "motivo": "The petition text is too short or empty to classify.",
                "palabras_clave": []
            }
        
        try:
            # Build enhanced system prompt with knowledge base context
            system_prompt = self.SYSTEM_PROMPT
            
            # Add knowledge base context if available
            if self.knowledge_base and self.knowledge_base.is_available():
                reference_context = self.knowledge_base.get_reference_context()
                if reference_context:
                    system_prompt += f"\n\n### DOCUMENTO DE REFERENCIA ADICIONAL\nTienes acceso al documento oficial de dependencias de ICETEX con información detallada:\n\n{reference_context}\n\nUsa esta información detallada para hacer clasificaciones más precisas. Todas las respuestas deben estar en español."
            
            # Call OpenAI API using legacy API
            response = self.client.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Classify this petition:\n\n{petition_text}"}
                ],
                temperature=0.3
            )
            result_text = response.choices[0].message.content
            
            result = json.loads(result_text)
            
            # Validate required fields
            required_fields = ["dependencia", "confianza", "motivo", "palabras_clave"]
            for field in required_fields:
                if field not in result:
                    result[field] = "N/A" if field != "palabras_clave" else []
            
            return result
            
        except json.JSONDecodeError as e:
            return {
                "dependencia": "Error",
                "confianza": "0%",
                "motivo": f"Failed to parse OpenAI response as JSON: {str(e)}",
                "palabras_clave": []
            }
        except Exception as e:
            return {
                "dependencia": "Error",
                "confianza": "0%",
                "motivo": f"Classification error: {str(e)}",
                "palabras_clave": []
            }
    
    def classify_with_metadata(self, petition_text: str) -> Dict[str, Any]:
        """
        Classify a petition and return additional metadata.
        
        Returns:
            Dictionary with classification and metadata (tokens used, model, etc.)
        """
        result = self.classify(petition_text)
        
        return {
            "classification": result,
            "metadata": {
                "model": self.model,
                "text_length": len(petition_text),
                "text_preview": petition_text[:200] + "..." if len(petition_text) > 200 else petition_text
            }
        }

