# ⚡ Quick Start Guide

Get the ICETEX Petition Classifier running in 5 minutes!

---

## 🚀 Super Quick Setup (macOS)

```bash
# 1. Install system dependencies
brew install python tesseract tesseract-lang poppler

# 2. Run automated setup
./setup.sh

# 3. Add your OpenAI API key to .env file
# (Edit the .env file that was created, or use the template)

# 4. Start the application
./start.sh
```

Now open http://localhost:8000 in your browser!

---

## 📝 Step-by-Step Setup

### Step 1: Install Prerequisites

**macOS:**
```bash
brew install python tesseract tesseract-lang poppler
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-venv tesseract-ocr tesseract-ocr-spa poppler-utils
```

### Step 2: Set Up Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

### Step 3: Install Python Packages

```bash
pip install -r requirements.txt
```

### Step 4: Configure OpenAI API Key

Create a `.env` file:

```bash
# Copy the template
cp env_template.txt .env

# Edit .env and add your API key
nano .env
```

Add your key:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-4-turbo
```

Get your API key here: https://platform.openai.com/api-keys

### Step 5: Start the Server

```bash
python main.py
```

Or use uvicorn directly:
```bash
uvicorn main:app --reload
```

### Step 6: Use the Application

Open your browser and go to:
```
http://localhost:8000
```

Upload a PDF petition and see the AI classify it!

---

## 🎯 Testing the System

### Test Petition Examples

Create test PDFs with the following content to verify classification:

**Test 1: Condonación Request**
```
Solicito la condonación del crédito educativo otorgado mediante 
el Fondo Bicentenario del Distrito de Cartagena.
```
Expected: **Vicepresidencia de Fondos en Administración**

**Test 2: Legal Issue**
```
Interpongo recurso de apelación contra la resolución 123 que 
niega mi solicitud de reclamación.
```
Expected: **Oficina Asesora Jurídica**

**Test 3: Technical Problem**
```
Reporto que la plataforma digital de ICETEX presenta errores 
técnicos al intentar cargar documentos.
```
Expected: **Vicepresidencia de Operaciones y Tecnología**

**Test 4: Payment Issue**
```
Solicito acuerdo de pago para la deuda en mora de mi 
crédito educativo.
```
Expected: **Vicepresidencia de Crédito y Cobranza**

---

## 🔍 Verify Installation

Run health check:
```bash
curl http://localhost:8000/health
```

Should return:
```json
{
  "status": "healthy",
  "openai_configured": true,
  "model": "gpt-4-turbo"
}
```

---

## ❓ Common Issues

### "Tesseract not found"
```bash
# macOS
brew install tesseract

# Verify
tesseract --version
```

### "Poppler not found"
```bash
# macOS
brew install poppler

# Verify
pdfinfo -v
```

### "OpenAI API key not configured"
- Make sure you created the `.env` file
- Check that your API key is correct
- Restart the server after adding the key

---

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [API endpoints documentation](#) at http://localhost:8000/docs
- Review the classification rules in `utils/openai_classifier.py`

---

## 💡 Pro Tips

1. **Use the automated scripts:**
   - `./setup.sh` - One-time setup
   - `./start.sh` - Quick start anytime

2. **Keep terminal open** to see processing logs

3. **Test with both text and scanned PDFs** to see OCR in action

4. **Monitor API costs** at https://platform.openai.com/usage

---

**Need help?** See the [Troubleshooting section](README.md#-troubleshooting) in README.md

