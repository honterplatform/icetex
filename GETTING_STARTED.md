# ✅ Getting Started Checklist

Follow these steps to get your ICETEX Petition Classifier up and running!

---

## 🎯 Prerequisites Checklist

Before you begin, make sure you have:

- [ ] **Python 3.11 or higher** installed
  ```bash
  python3 --version
  ```

- [ ] **OpenAI API Key** from https://platform.openai.com/api-keys
  - [ ] Sign up/log in to OpenAI
  - [ ] Create a new API key
  - [ ] Copy it somewhere safe

- [ ] **Homebrew** installed (macOS only)
  ```bash
  brew --version
  ```

---

## 📦 System Dependencies (macOS)

Run these commands in Terminal:

```bash
# Install Tesseract OCR (for scanned PDFs)
brew install tesseract tesseract-lang

# Install Poppler (for PDF to image conversion)
brew install poppler

# Verify installations
tesseract --version
pdfinfo -v
```

**Ubuntu/Debian users**: See README.md for apt-get commands

---

## 🚀 Quick Installation (Automated)

### Option A: One-Command Setup (Recommended)

```bash
cd "/Users/axel/Documents/AXEL TRUJILLO/ICETEX/PLATAFORMA PETICIONES AI"
./setup.sh
```

This script will:
1. ✅ Check your Python version
2. ✅ Check for Tesseract and Poppler
3. ✅ Create virtual environment
4. ✅ Install all dependencies
5. ✅ Help you create .env file

Then start the app:
```bash
./start.sh
```

---

## 🔧 Manual Installation (Step by Step)

If you prefer manual control:

### Step 1: Navigate to Project
```bash
cd "/Users/axel/Documents/AXEL TRUJILLO/ICETEX/PLATAFORMA PETICIONES AI"
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
```

### Step 3: Activate Virtual Environment
```bash
source venv/bin/activate
```
Your prompt should now show `(venv)`

### Step 4: Install Python Packages
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Create .env File
```bash
# Copy the template
cp env_template.txt .env

# Edit with your favorite editor
nano .env
# or
open .env
```

Add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-4-turbo
```

Save and close the file.

### Step 6: Start the Server
```bash
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 7: Open in Browser
Open your browser and go to:
```
http://localhost:8000
```

---

## ✅ Verify Installation

### Test 1: Health Check
Open a new terminal and run:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "openai_configured": true,
  "model": "gpt-4-turbo"
}
```

### Test 2: Dependencies List
```bash
curl http://localhost:8000/dependencies
```

Should return a list of all 12 ICETEX dependencies.

### Test 3: Upload a Test PDF
1. Go to http://localhost:8000
2. Upload a PDF petition
3. Click "Clasificar Petición"
4. Wait for results (3-15 seconds)
5. Results should display with dependency, confidence, and explanation

---

## 📝 Create a Test Petition

If you don't have a PDF to test, create one with this content:

**Test Petition 1: Condonación**
```
PETICIÓN

Señores ICETEX:

Por medio de la presente, solicito la condonación del crédito educativo 
otorgado mediante el Fondo Bicentenario del Distrito de Cartagena, según 
lo establecido en el convenio 123 de 2020.

Agradezco su atención.

Atentamente,
Juan Pérez
```

Save as PDF and upload to test.

**Expected Result**: Vicepresidencia de Fondos en Administración

---

## 🎨 What You Should See

### Upload Page
- Beautiful gradient background (purple)
- White card with ICETEX title
- Upload area with cloud icon
- "Haga clic o arrastre un archivo PDF aquí"

### Results Page
- Green success icon
- Dependency name (large, blue)
- Confidence percentage (large, green)
- Explanation paragraph
- Keyword badges (purple pills)
- Reset button

---

## 🐛 Common Issues & Solutions

### Issue: "Command not found: python3"
**Solution**: Install Python from https://www.python.org/downloads/

### Issue: "Tesseract not found"
**Solution**: 
```bash
brew install tesseract
```

### Issue: "Poppler not found"
**Solution**:
```bash
brew install poppler
```

### Issue: "OpenAI API key not configured"
**Solution**: 
1. Check that .env file exists
2. Verify API key is correct (starts with `sk-`)
3. Restart the server

### Issue: "Port 8000 already in use"
**Solution**: 
```bash
# Find what's using port 8000
lsof -i :8000

# Kill the process (replace PID with actual number)
kill -9 PID

# Or use a different port
uvicorn main:app --port 8001
```

### Issue: "Could not extract text from PDF"
**Possible causes**:
- PDF is password-protected → Remove password
- PDF is corrupted → Try different PDF
- Scanned PDF with poor quality → Improve scan quality

---

## 📊 Your First Classification

### Step-by-Step Test

1. **Start the server**
   ```bash
   ./start.sh
   ```

2. **Open browser**
   ```
   http://localhost:8000
   ```

3. **Prepare a test PDF** with one of these texts:
   - "Solicito condonación del crédito del Fondo X"
   - "Interpongo recurso de apelación contra resolución"
   - "La plataforma presenta errores técnicos"

4. **Upload the PDF**
   - Drag & drop OR click upload area
   - Select your PDF file

5. **Click "Clasificar Petición"**
   - Wait for processing (3-15 seconds)
   - Watch the loading spinner

6. **Review results**
   - Check the dependency assignment
   - Review confidence level
   - Read the explanation
   - See detected keywords

7. **Test another petition**
   - Click "Clasificar Otra Petición"
   - Upload a different PDF

---

## 🎓 Understanding the Results

### Dependencia (Dependency)
The ICETEX office assigned to handle the petition.

### Confianza (Confidence)
How certain the AI is about the classification:
- **90-100%**: Very confident
- **75-89%**: Confident
- **60-74%**: Moderately confident
- **< 60%**: Low confidence (might need manual review)

### Motivo (Reason)
Natural language explanation of why this dependency was chosen.

### Palabras Clave (Keywords)
Important words detected that influenced the classification.

---

## 🎯 Next Steps After Setup

### For Testing
1. [ ] Test with various petition types
2. [ ] Try both text and scanned PDFs
3. [ ] Verify all 12 dependencies can be classified
4. [ ] Check response times

### For Production
1. [ ] Set up proper API key management
2. [ ] Configure rate limiting
3. [ ] Set up monitoring
4. [ ] Create backup strategy
5. [ ] Document custom workflows

### For Customization
1. [ ] Adjust system prompt if needed (utils/openai_classifier.py)
2. [ ] Customize UI colors (templates/upload.html)
3. [ ] Add your logo
4. [ ] Configure additional settings

---

## 📚 Documentation Reference

- **Full Documentation**: README.md
- **Quick Reference**: QUICKSTART.md
- **Workflow Details**: WORKFLOW.md
- **Project Overview**: PROJECT_SUMMARY.md
- **This Guide**: GETTING_STARTED.md

---

## 💡 Pro Tips

1. **Keep the terminal open** to see processing logs
2. **Test with diverse petitions** to ensure accuracy
3. **Monitor API costs** at https://platform.openai.com/usage
4. **Save successful test cases** for future reference
5. **Read the logs** if something goes wrong

---

## ✨ You're Ready!

Congratulations! Your ICETEX Petition Classifier is now set up and ready to use.

**Quick Start Command:**
```bash
./start.sh
```

**Access URL:**
```
http://localhost:8000
```

---

## 🆘 Need Help?

1. **Check documentation**: README.md has detailed troubleshooting
2. **Review logs**: Terminal shows detailed error messages
3. **Test health endpoint**: `curl http://localhost:8000/health`
4. **Verify dependencies**: Run `./setup.sh` again

---

**Happy Classifying! 🎓**

