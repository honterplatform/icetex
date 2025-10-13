# 🔄 ICETEX Petition Classifier - Workflow Guide

This document explains the complete workflow of the petition classification system.

---

## 📊 System Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                         START                                   │
│              User opens http://localhost:8000                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  STEP 1: UPLOAD INTERFACE                       │
│                                                                 │
│  ┌───────────────────────────────────────────────────────┐    │
│  │  🎓 Clasificador de Peticiones ICETEX                 │    │
│  │                                                        │    │
│  │  ╔══════════════════════════════════════════════╗     │    │
│  │  ║  ☁️  Haga clic o arrastre un archivo PDF    ║     │    │
│  │  ║     Acepta PDFs con texto o escaneados       ║     │    │
│  │  ╚══════════════════════════════════════════════╝     │    │
│  │                                                        │    │
│  │  [Clasificar Petición]                                │    │
│  └───────────────────────────────────────────────────────┘    │
└────────────────────────┬────────────────────────────────────────┘
                         │ User selects/drops PDF
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  STEP 2: FILE VALIDATION                        │
│                                                                 │
│  ✓ Check file type (must be .pdf)                             │
│  ✓ Check file size (not empty)                                │
│  ✓ Prepare for upload                                          │
└────────────────────────┬────────────────────────────────────────┘
                         │ Validation passed
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  STEP 3: PROCESSING                             │
│                                                                 │
│  🔄 Procesando PDF y clasificando con IA...                    │
│     Esto puede tomar unos segundos                             │
│                                                                 │
│  Backend Process:                                               │
│  1. Receive PDF file                                            │
│  2. Save to temporary location                                  │
│  3. Extract text → See "Text Extraction Flow" below            │
│  4. Send to OpenAI → See "AI Classification Flow" below        │
│  5. Clean up temporary files                                    │
└────────────────────────┬────────────────────────────────────────┘
                         │ Processing complete
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  STEP 4: DISPLAY RESULTS                        │
│                                                                 │
│  ✅ Resultado de la Clasificación                              │
│                                                                 │
│  Dependencia Asignada:                                          │
│  ► Vicepresidencia de Fondos en Administración                 │
│                                                                 │
│  Nivel de Confianza:                                            │
│  ► 95%                                                          │
│                                                                 │
│  Justificación:                                                 │
│  ► The petition requests forgiveness (condonación) of...       │
│                                                                 │
│  Palabras Clave:                                                │
│  ► [condonación] [fondo] [crédito educativo]                   │
│                                                                 │
│  [Clasificar Otra Petición]                                    │
└────────────────────────┬────────────────────────────────────────┘
                         │ User clicks reset
                         ▼
                    Back to STEP 1
```

---

## 📄 Text Extraction Flow

```
PDF File Received
    │
    ▼
┌─────────────────────────────────────┐
│  Try pdfplumber (Text Extraction)   │
│  Fast method for digital PDFs       │
└───────────┬─────────────────────────┘
            │
            ▼
    Text extracted? (>100 chars)
            │
            ├─ YES ─────────────────────┐
            │                           │
            └─ NO                       │
                │                       │
                ▼                       │
    ┌─────────────────────────┐       │
    │  Convert PDF to Images   │       │
    │  (pdf2image + Poppler)  │       │
    └──────────┬──────────────┘       │
               │                       │
               ▼                       │
    ┌─────────────────────────┐       │
    │  Run OCR on each page   │       │
    │  (pytesseract)          │       │
    │  Language: Spanish      │       │
    └──────────┬──────────────┘       │
               │                       │
               ▼                       │
    ┌─────────────────────────┐       │
    │  Combine all page texts │       │
    └──────────┬──────────────┘       │
               │                       │
               └───────────────────────┤
                                       │
                                       ▼
                            ┌──────────────────┐
                            │  Extracted Text  │
                            │  (Ready for AI)  │
                            └──────────────────┘
```

---

## 🤖 AI Classification Flow

```
Extracted Text Received
    │
    ▼
┌─────────────────────────────────────────────┐
│  Prepare OpenAI API Call                    │
│  - Model: gpt-4-turbo                       │
│  - Temperature: 0.3 (consistent results)    │
│  - Response format: JSON                    │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  System Prompt (Rules & Context)            │
│                                             │
│  "You are an AI classification system..."  │
│  + 12 classification rules                  │
│  + Example classifications                  │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  User Message                               │
│  "Classify this petition:"                  │
│  + Full extracted text                      │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  Send to OpenAI API                         │
│  (Network request)                          │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  Receive JSON Response                      │
│  {                                          │
│    "dependencia": "...",                    │
│    "confianza": "XX%",                      │
│    "motivo": "...",                         │
│    "palabras_clave": [...]                  │
│  }                                          │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  Validate Response                          │
│  - Check all required fields present        │
│  - Validate JSON structure                  │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  Add Metadata                               │
│  - Model used                               │
│  - Text length                              │
│  - Text preview                             │
│  - Original filename                        │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  Return to Frontend                         │
│  Complete classification result             │
└─────────────────────────────────────────────┘
```

---

## 🎯 Decision Rules (AI Classification)

The AI uses these rules to classify petitions:

### Rule 1: Fondos y Condonación
**Keywords**: fondos, convenios, condonación, becas, crédito condonable  
**→ Vicepresidencia de Fondos en Administración**

Example: "Solicito la condonación del crédito del Fondo Bicentenario"

### Rule 2: Legal Matters
**Keywords**: demanda, sanción, resolución, fallo, normatividad, derecho, apelación, abogado  
**→ Oficina Asesora Jurídica**

Example: "Interpongo recurso de apelación contra la resolución 123"

### Rule 3: Risk & Internal Control
**Keywords**: riesgos, cumplimiento, control interno, auditoría, transparencia  
**→ Oficina de Riesgos** or **Oficina de Control Interno**

Example: "Solicito auditoría del proceso de selección"

### Rule 4: Planning
**Keywords**: planeación, estrategia, indicadores, metas institucionales  
**→ Oficina Asesora de Planeación**

Example: "Propuesta para mejorar indicadores de gestión"

### Rule 5: Technology
**Keywords**: tecnología, plataforma, sistema, errores técnicos, mantenimiento  
**→ Vicepresidencia de Operaciones y Tecnología**

Example: "La plataforma presenta errores al cargar documentos"

### Rule 6: Communications
**Keywords**: comunicación, prensa, medios, campañas  
**→ Oficina Asesora de Comunicaciones**

Example: "Solicito nota de prensa sobre nuevo programa"

### Rule 7: Collections
**Keywords**: cobro, mora, pagos, deudas, cartera  
**→ Vicepresidencia de Crédito y Cobranza**

Example: "Solicito acuerdo de pago para deuda en mora"

### Rule 8: Finance
**Keywords**: presupuesto, finanzas, tesorería, contabilidad  
**→ Vicepresidencia Financiera**

Example: "Consulta sobre estado de cuenta y saldos"

### Rule 9: International
**Keywords**: internacional, becas en el exterior, cooperación  
**→ Oficina de Relaciones Internacionales**

Example: "Información sobre becas de maestría en España"

### Rule 10: Commercial
**Keywords**: comercial, mercadeo, usuarios, aliados estratégicos  
**→ Oficina Comercial y de Mercadeo**

Example: "Propuesta de alianza estratégica con universidad"

### Rule 11: HR & Records
**Keywords**: personal, contratación, archivos, secretaría  
**→ Secretaría General**

Example: "Solicito copia certificada de contrato"

### Rule 12: Ambiguous Cases
If the petition matches multiple categories or is unclear:
- AI selects the most probable dependency
- Lowers confidence level accordingly
- Provides detailed explanation

---

## 📊 Example Processing Times

### Scenario A: Digital PDF (5 pages)
```
Upload:           0.5s
Text Extraction:  1.0s (pdfplumber)
AI Classification: 2.5s
Display Results:   0.5s
──────────────────────
TOTAL:            4.5s
```

### Scenario B: Scanned PDF (5 pages)
```
Upload:           0.5s
PDF to Images:    2.0s
OCR Processing:   8.0s (pytesseract)
AI Classification: 2.5s
Display Results:   0.5s
──────────────────────
TOTAL:           13.5s
```

---

## 🔄 User Interaction Flow

```
1. User arrives at homepage
   └─→ Sees upload interface
   
2. User uploads PDF
   ├─→ Drag & drop OR
   └─→ Click to browse
   
3. File selected
   └─→ Filename displayed
   └─→ "Clasificar Petición" button enabled
   
4. User clicks "Clasificar Petición"
   └─→ Loading spinner appears
   └─→ Upload form disabled
   
5. Processing happens
   └─→ Progress message shown
   └─→ User waits (3-15 seconds)
   
6. Results displayed
   └─→ Dependency highlighted
   └─→ Confidence shown
   └─→ Explanation provided
   └─→ Keywords listed
   
7. User options:
   ├─→ Review results
   └─→ Click "Clasificar Otra Petición"
       └─→ Returns to step 1
```

---

## 🎨 UI States

### State 1: Initial (Ready for Upload)
- Upload area: Visible, interactive
- Submit button: Enabled
- Results: Hidden
- Loading: Hidden
- Error: Hidden

### State 2: File Selected
- Upload area: Shows selected filename
- Submit button: Enabled, highlighted
- Results: Hidden
- Loading: Hidden
- Error: Hidden

### State 3: Processing
- Upload area: Disabled
- Submit button: Disabled
- Results: Hidden
- Loading: **Visible with spinner**
- Error: Hidden

### State 4: Success
- Upload area: Hidden
- Submit button: Hidden
- Results: **Visible with data**
- Loading: Hidden
- Error: Hidden

### State 5: Error
- Upload area: Visible
- Submit button: Enabled
- Results: Hidden
- Loading: Hidden
- Error: **Visible with message**

---

## 🔐 Security Flow

```
PDF Upload Request
    │
    ▼
┌─────────────────────────┐
│  Validate File Type     │
│  Must be .pdf           │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Validate File Size     │
│  Must not be empty      │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Save to Temp Location  │
│  Isolated from system   │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Process PDF            │
│  Extract text only      │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Delete Temp File       │
│  Immediate cleanup      │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Send Text to OpenAI    │
│  API key from .env      │
│  Never exposed to user  │
└─────────────────────────┘
```

---

## 🎯 Success Criteria Checklist

For each petition classification, the system must:

- [ ] Accept the PDF file successfully
- [ ] Extract readable text (>10 characters)
- [ ] Send text to OpenAI API
- [ ] Receive valid JSON response
- [ ] Display dependency name
- [ ] Display confidence percentage
- [ ] Display natural language explanation
- [ ] Display detected keywords (if any)
- [ ] Allow user to reset and classify another
- [ ] Clean up temporary files
- [ ] Handle errors gracefully

---

## 💡 Tips for Best Results

### For Users
1. **Use clear, well-written petitions**
2. **Ensure scanned PDFs are high quality** (300 DPI+)
3. **Include relevant keywords** in petition text
4. **Write in Spanish** (system is optimized for Spanish)

### For Administrators
1. **Monitor OpenAI API costs** at platform.openai.com
2. **Check server logs** for processing issues
3. **Test with various PDF types** regularly
4. **Update system prompt** if classification rules change

---

## 🚀 Performance Optimization

### Current Performance
- Text PDF: ~4-5 seconds
- Scanned PDF: ~13-15 seconds

### Optimization Opportunities
1. **Implement caching** for repeated petitions
2. **Use async processing** for multiple uploads
3. **Add progress indicators** for long OCR processes
4. **Optimize image quality** for OCR (balance quality/speed)
5. **Consider GPT-3.5-turbo** for simpler cases

---

**Ready to classify petitions? Start the server and upload a PDF!**

```bash
./start.sh
```

Then open: http://localhost:8000

