# 🎓 ICETEX Petition Classifier

An intelligent AI-powered system that automatically classifies PDF petitions directed to ICETEX and determines which internal dependency (office) should handle each petition.

Built with **Python**, **FastAPI**, and **OpenAI GPT-4**.

---

## 📋 Features

- ✅ **PDF Upload Interface**: Modern drag-and-drop web interface for uploading petitions
- 🔍 **Smart Text Extraction**: Handles both text-based PDFs (pdfplumber) and scanned PDFs (OCR with pytesseract)
- 🤖 **AI Classification**: Uses OpenAI GPT-4 to classify petitions based on ICETEX's "Manual de Funciones y Competencias Laborales V2"
- 📊 **Detailed Results**: Returns dependency assignment, confidence level, justification, and detected keywords
- ⚡ **Fast & Lightweight**: Local web application with minimal dependencies

---

## 🏢 ICETEX Dependencies Covered

The system classifies petitions into 12 main ICETEX offices:

1. **Oficina Asesora Jurídica** — Legal matters, contracts, litigation
2. **Oficina Asesora de Planeación** — Strategic planning, performance indicators
3. **Oficina Asesora de Comunicaciones** — Press, public relations, communications
4. **Oficina de Riesgos** — Risk management, compliance
5. **Oficina de Control Interno** — Audits, internal oversight
6. **Oficina de Relaciones Internacionales** — International scholarships, cooperation
7. **Oficina Comercial y de Mercadeo** — Marketing, user acquisition
8. **Vicepresidencia de Crédito y Cobranza** — Credit, collections, payment agreements
9. **Vicepresidencia de Operaciones y Tecnología** — IT systems, platform maintenance
10. **Vicepresidencia Financiera** — Treasury, accounting, budget
11. **Vicepresidencia de Fondos en Administración** — Fund management, condonación processes
12. **Secretaría General** — Contracts, records, HR, administrative coordination

---

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.11+**
   ```bash
   python --version
   ```

2. **Tesseract OCR** (for scanned PDFs)
   - **macOS**: 
     ```bash
     brew install tesseract tesseract-lang
     ```
   - **Ubuntu/Debian**:
     ```bash
     sudo apt-get install tesseract-ocr tesseract-ocr-spa
     ```
   - **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

3. **Poppler** (for PDF to image conversion)
   - **macOS**:
     ```bash
     brew install poppler
     ```
   - **Ubuntu/Debian**:
     ```bash
     sudo apt-get install poppler-utils
     ```
   - **Windows**: Download from [poppler releases](http://blog.alivate.com.au/poppler-windows/)

4. **OpenAI API Key**
   - Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)

---

## 📦 Installation

### Step 1: Clone or Download the Project

```bash
cd /Users/axel/Documents/AXEL\ TRUJILLO/ICETEX/PLATAFORMA\ PETICIONES\ AI
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```bash
touch .env
```

Add your OpenAI API key:

```env
# .env file
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4-turbo
```

> ⚠️ **Important**: Never commit your `.env` file to version control. It's already in `.gitignore`.

---

## 🎮 Usage

### Start the Server

```bash
python main.py
```

Or with uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Access the Application

Open your browser and navigate to:

```
http://localhost:8000
```

### Using the Interface

1. **Upload a PDF**: Drag and drop or click to select a PDF petition file
2. **Submit**: Click "Clasificar Petición" to process the document
3. **View Results**: The system will display:
   - The assigned ICETEX dependency
   - Confidence level (percentage)
   - Justification for the classification
   - Detected keywords from the petition

---

## 📡 API Endpoints

### `GET /`
Returns the upload form (HTML interface)

### `POST /classify`
Classifies an uploaded PDF petition

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: PDF file

**Response:**
```json
{
  "classification": {
    "dependencia": "Vicepresidencia de Fondos en Administración",
    "confianza": "95%",
    "motivo": "The document mentions condonación and Fondo Bicentenario, which clearly falls under managed funds.",
    "palabras_clave": ["condonación", "fondo", "crédito educativo"]
  },
  "metadata": {
    "model": "gpt-4-turbo",
    "text_length": 1243,
    "text_preview": "Solicito la condonación del crédito..."
  },
  "filename": "petition.pdf"
}
```

### `GET /health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "openai_configured": true,
  "model": "gpt-4-turbo"
}
```

### `GET /dependencies`
Lists all ICETEX dependencies with descriptions

---

## 🧪 Testing the System

### Test with Example Petitions

You can test the system with various petition types:

1. **Condonación request**: Should route to "Vicepresidencia de Fondos en Administración"
2. **Legal complaint**: Should route to "Oficina Asesora Jurídica"
3. **Technical issue**: Should route to "Vicepresidencia de Operaciones y Tecnología"
4. **Payment issue**: Should route to "Vicepresidencia de Crédito y Cobranza"

### Command-Line Testing

You can also test the API with curl:

```bash
curl -X POST "http://localhost:8000/classify" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/petition.pdf"
```

---

## 🏗️ Project Structure

```
PLATAFORMA PETICIONES AI/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── templates/             # HTML templates
│   └── upload.html        # Main upload interface
└── utils/                 # Utility modules
    ├── __init__.py        # Package initializer
    ├── pdf_extractor.py   # PDF text extraction logic
    └── openai_classifier.py  # OpenAI API integration
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | - | ✅ Yes |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4-turbo` | No |

### Customizing Tesseract Path

If Tesseract is not in your PATH, you can set it manually in `utils/pdf_extractor.py`:

```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'/custom/path/to/tesseract'
```

---

## 🐛 Troubleshooting

### Issue: "Tesseract not found"

**Solution**: Install Tesseract OCR and ensure it's in your PATH:

```bash
# macOS
brew install tesseract

# Verify installation
tesseract --version
```

### Issue: "Could not extract text from PDF"

**Possible causes**:
1. PDF is password-protected
2. PDF is corrupted
3. Scanned PDF with poor image quality

**Solution**: Try with a different PDF or improve scan quality.

### Issue: "OpenAI API key not configured"

**Solution**: 
1. Create a `.env` file in the project root
2. Add your API key: `OPENAI_API_KEY=sk-...`
3. Restart the server

### Issue: "Poppler not found" (pdf2image error)

**Solution**: Install Poppler:

```bash
# macOS
brew install poppler

# Ubuntu/Debian
sudo apt-get install poppler-utils
```

---

## 💰 Cost Considerations

### OpenAI API Costs

- **Model**: GPT-4-turbo
- **Estimated cost per petition**: $0.01 - $0.05 (depending on text length)
- **Input tokens**: ~500-2000 per petition
- **Output tokens**: ~100-200 per response

Check current pricing at [OpenAI Pricing](https://openai.com/pricing)

### Optimization Tips

1. Use `gpt-3.5-turbo` for lower costs (less accurate)
2. Implement caching for repeated petitions
3. Batch process petitions during off-peak hours

---

## 🔐 Security Considerations

1. **API Key Protection**: Never commit `.env` file or expose API keys
2. **File Upload Limits**: Consider adding file size limits in production
3. **Rate Limiting**: Implement rate limiting for public deployments
4. **Input Validation**: All uploads are validated as PDF files
5. **Temporary Files**: Uploaded files are automatically cleaned up

---

## 🚀 Production Deployment

### Using Gunicorn (Recommended for production)

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-spa \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t icetex-classifier .
docker run -p 8000:8000 --env-file .env icetex-classifier
```

---

## 📈 Future Enhancements

- [ ] Add user authentication and session management
- [ ] Implement petition history and tracking
- [ ] Add batch processing for multiple PDFs
- [ ] Create API documentation with Swagger UI
- [ ] Add support for other document formats (Word, images)
- [ ] Implement caching to reduce API costs
- [ ] Add analytics dashboard for classification statistics
- [ ] Multi-language support (currently optimized for Spanish)

---

## 📄 License

This project is for internal ICETEX use. All rights reserved.

---

## 👨‍💻 Technical Support

For issues or questions:

1. Check the **Troubleshooting** section above
2. Review OpenAI API documentation
3. Ensure all prerequisites are properly installed
4. Check server logs for detailed error messages

---

## 🙏 Acknowledgments

- **FastAPI**: Modern web framework for Python
- **OpenAI**: GPT-4 language model
- **pdfplumber**: PDF text extraction
- **Tesseract OCR**: Optical character recognition
- **ICETEX**: Manual de Funciones y Competencias Laborales V2

---

**Built with ❤️ for ICETEX**

