# 🚀 Deployment Guide - Excel Search Feature

This guide explains how to deploy the platform with the Excel search feature so it works from anywhere in the world.

## 📋 Overview

When deployed, the search page will be accessible from **any browser, anywhere**, and it will fetch data from the Excel file that's deployed with the application.

---

## ✅ Pre-Deployment Checklist

### 1. **Place Your Excel File**
Make sure your Excel file is in the `data/` folder:
```
PLATAFORMA PETICIONES AI/
├── main.py
├── data/
│   └── contratos_icetex.xlsx  ← MUST be here before deployment
└── ...
```

### 2. **Verify File is NOT Ignored**
The `.gitignore` should NOT exclude Excel files. Your Excel file should be committed to git/deployed.

### 3. **Test Locally First**
Before deploying, test locally:
```bash
python main.py
```
Then visit: `http://localhost:8000/search`
Verify searches work correctly.

---

## 🌐 Deployment Options

### Option 1: Railway (Recommended)

1. **Add Excel File to Repository**
   ```bash
   git add data/contratos_icetex.xlsx
   git commit -m "Add Excel data file"
   git push
   ```

2. **Deploy to Railway**
   - Connect your repository to Railway
   - Railway will use the `Dockerfile` automatically
   - The Excel file will be included in the deployment

3. **Set Environment Variables** (if needed)
   In Railway dashboard, add:
   ```
   OPENAI_API_KEY=your-key-here
   EXCEL_FILE_PATH=  (leave empty for default: data/contratos_icetex.xlsx)
   ```

4. **Access Your Application**
   - Railway provides a public URL (e.g., `https://your-app.railway.app`)
   - Anyone can access: `https://your-app.railway.app/search`
   - The search will work from anywhere!

---

### Option 2: Docker Deployment

1. **Build the Docker Image**
   ```bash
   docker build -t icetex-platform .
   ```

2. **Run the Container**
   ```bash
   docker run -d \
     -p 8000:8000 \
     -e OPENAI_API_KEY=your-key-here \
     -e EXCEL_FILE_PATH=  \
     --name icetex-app \
     icetex-platform
   ```

3. **The Excel file is included** in the Docker image (from `COPY . .`)

4. **Access the Application**
   - Local: `http://localhost:8000/search`
   - Public: Configure port forwarding or use a reverse proxy

---

### Option 3: Cloud Platforms (Heroku, AWS, GCP, Azure)

#### Heroku
1. **Add Excel file to git**:
   ```bash
   git add data/contratos_icetex.xlsx
   git commit -m "Add Excel data file"
   git push heroku main
   ```

2. **The Excel file will be included** in the deployment

#### AWS/GCP/Azure
- Deploy using Docker or directly
- Ensure `data/contratos_icetex.xlsx` is included in the deployment package
- The file path (`data/contratos_icetex.xlsx`) is relative to where the app runs

---

## 🔍 How It Works

### Architecture:
```
Internet User (Anywhere)
    ↓
    ↓ Types: https://your-app.com/search
    ↓
    ↓ Enters search term
    ↓
FastAPI Backend (Running on Server)
    ↓
    ↓ Reads from: data/contratos_icetex.xlsx
    ↓
    ↓ Searches Excel file
    ↓
    ↓ Returns results
    ↓
User's Browser (Sees Results)
```

### Key Points:
1. **The Excel file is deployed WITH the application** - it's part of the codebase
2. **The file path is relative** - works regardless of server location
3. **The backend reads from disk** - fast, no external database needed
4. **Any user can search** - as long as they have the URL

---

## 📁 File Path Resolution

The system uses **relative paths**, so it works anywhere:

```python
# In utils/excel_search.py
project_root = Path(__file__).parent.parent
excel_file_path = project_root / "data" / "contratos_icetex.xlsx"
```

This means:
- ✅ Works on your local machine
- ✅ Works on Railway
- ✅ Works on AWS/GCP/Azure
- ✅ Works in Docker containers
- ✅ Works on any server, anywhere

---

## 🔄 Updating the Excel File

When you need to update the Excel file:

### For Deployed Applications:

**Option 1: Re-deploy** (Recommended)
1. Replace `data/contratos_icetex.xlsx` with new file
2. Commit and push changes
3. Re-deploy application
4. The new file will be used automatically

**Option 2: Use Environment Variable** (For frequent updates)
1. Upload new Excel to cloud storage (S3, etc.)
2. Set `EXCEL_FILE_PATH` environment variable to the URL/path
3. Restart application

---

## ✅ Verification

After deployment, verify:

1. **Check the search page loads:**
   ```
   https://your-app.com/search
   ```

2. **Test a search:**
   - Try searching by name or ID
   - Should return results from your Excel file

3. **Check logs** (if available):
   ```
   ✅ Excel file loaded successfully: X rows, Y columns
   ```

---

## 🐛 Troubleshooting

### Issue: "Excel file not found" after deployment

**Solution:**
1. Verify the file is in `data/` folder locally
2. Check that `data/contratos_icetex.xlsx` is committed to git
3. Verify the file is included in deployment (check deployment logs)
4. Check file permissions on the server

### Issue: Search returns no results

**Solution:**
1. Verify the Excel file loaded (check `/api/excel-info` endpoint)
2. Check that your search terms match the data format
3. Verify column names are correct

### Issue: File too large for deployment

**Solution:**
1. Consider using environment variable with cloud storage
2. Or use a database instead of Excel file
3. Or compress the Excel file

---

## 🔒 Security Considerations

1. **Excel file is public** - anyone with the URL can search it
2. **Consider authentication** if data is sensitive
3. **Rate limiting** recommended for public deployments
4. **The Excel file is in the codebase** - ensure it doesn't contain sensitive data or use `.gitignore` if needed

---

## 📊 Expected Behavior

### ✅ What Works:
- ✅ Search from any browser, anywhere
- ✅ Multiple users can search simultaneously
- ✅ Fast searches (file loaded in memory)
- ✅ Works on any platform (Windows, Mac, Linux servers)

### ⚠️ Limitations:
- Excel file must be updated via re-deployment (unless using external storage)
- File is loaded once at startup (requires restart to reload)
- File size limited by server memory

---

## 🎯 Summary

**To deploy with Excel search working from anywhere:**

1. ✅ Place Excel file in `data/contratos_icetex.xlsx`
2. ✅ Commit file to git
3. ✅ Deploy application (Railway, Docker, cloud platform)
4. ✅ Share the URL: `https://your-app.com/search`
5. ✅ Anyone can now search from anywhere!

The Excel file travels with your application, so it works everywhere! 🌍

