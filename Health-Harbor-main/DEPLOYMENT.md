# 🚀 Health Harbor Deployment Guide

Complete guide to deploy your Health Harbor application to production using **FREE** services.

---

## 📋 **Deployment Architecture**

```
Frontend (Vercel)          Backend (Render)              Database (Neon)
   React + Vite    ──────>   Flask + Python    ──────>   PostgreSQL
      FREE                      FREE                        FREE
```

---

## **Prerequisites**

- ✅ GitHub account
- ✅ Gemini API key (you already have this)
- ✅ Neon database (already configured)

---

## **Step 1: Prepare Your Code** 📦

### A. Push to GitHub

```powershell
# Navigate to your project
cd "d:\hackthon\Health-Harbor-main (2)\Health-Harbor-main"

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Health Harbor"

# Create GitHub repo at https://github.com/new
# Then link and push:
git remote add origin https://github.com/YOUR_USERNAME/health-harbor.git
git branch -M main
git push -u origin main
```

### B. Update .gitignore

Make sure these are in `.gitignore`:
```
.env
__pycache__/
*.pyc
node_modules/
dist/
.venv/
uploads/
*.pkl
```

---

## **Step 2: Deploy Backend to Render** 🔧

### Option A: Using Render Dashboard (Easiest)

1. **Go to [Render.com](https://render.com/)** and sign up (free)

2. **Click "New +"** → **"Web Service"**

3. **Connect GitHub** and select your repository

4. **Configure:**
   - **Name:** `health-harbor-backend`
   - **Region:** `Singapore` (closest to your Neon DB)
   - **Branch:** `main`
   - **Root Directory:** `vitalplunder/backend`
   - **Runtime:** `Python 3`
   - **Build Command:**
     ```bash
     pip install -r requirements.txt && python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('vader_lexicon'); nltk.download('brown')"
     ```
   - **Start Command:**
     ```bash
     gunicorn -b 0.0.0.0:$PORT app:create_app()
     ```

5. **Add Environment Variables:**
   Click "Environment" tab and add:
   
   | Key | Value |
   |-----|-------|
   | `SECRET_KEY` | `your-random-secret-key-here` |
   | `FLASK_DEBUG` | `False` |
   | `DATABASE_URL` | (copy from your .env file) |
   | `GEMINI_API_KEY` | `AIzaSyAUyShR1-T-4Q8oRsS1EY0YGZT05ohyozA` |
   | `CAPTAINS_LOG_TABLE_NAME` | `captains_log_entries` |
   | `PYTHON_VERSION` | `3.11.0` |

6. **Click "Create Web Service"**

7. **Wait 5-10 minutes** for deployment

8. **Copy your backend URL:** `https://health-harbor-backend.onrender.com`

### Option B: Using render.yaml (Auto-deploy)

The `render.yaml` file is already created. Just:

1. Push to GitHub
2. Go to Render Dashboard
3. Click "New" → "Blueprint"
4. Select your repo
5. Select `vitalplunder/backend/render.yaml`
6. Add environment variables in Render dashboard
7. Deploy!

---

## **Step 3: Deploy Frontend to Vercel** 🌐

1. **Go to [Vercel.com](https://vercel.com/)** and sign up (free)

2. **Click "Add New..."** → **"Project"**

3. **Import your GitHub repository**

4. **Configure:**
   - **Framework Preset:** `Vite`
   - **Root Directory:** `vitalplunder/frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`

5. **Add Environment Variables:**
   Click "Environment Variables" and add:
   
   | Key | Value |
   |-----|-------|
   | `VITE_API_BASE_URL` | `https://health-harbor-backend.onrender.com/api` |

   *(Replace with your actual Render backend URL from Step 2)*

6. **Click "Deploy"**

7. **Wait 2-3 minutes** for deployment

8. **Your app is live!** 🎉
   - URL: `https://health-harbor-yourname.vercel.app`

---

## **Step 4: Update Frontend API URL** 🔗

After backend deployment, update:

**File:** `vitalplunder/frontend/.env.production`
```env
VITE_API_BASE_URL=https://health-harbor-backend.onrender.com/api
```

Then redeploy frontend:
- Vercel auto-deploys on git push
- Or click "Redeploy" in Vercel dashboard

---

## **Step 5: Configure CORS** 🔐

Update backend CORS to allow your Vercel domain:

**File:** `vitalplunder/backend/app.py` (around line 60)

```python
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000", 
            "http://localhost:5173",
            "https://health-harbor-yourname.vercel.app",  # Add your Vercel URL
            "https://*.vercel.app"  # Allow all Vercel preview deployments
        ],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

Commit and push to trigger redeploy.

---

## **Alternative Deployment Options**

### Backend Alternatives:
- **Railway.app** - Similar to Render, easy deployment
- **Google Cloud Run** - Free tier, Docker-based (you already have Dockerfile!)
- **Fly.io** - Free tier, good for Python apps
- **PythonAnywhere** - Python-specific hosting

### Frontend Alternatives:
- **Netlify** - Similar to Vercel
- **Cloudflare Pages** - Free, fast CDN
- **GitHub Pages** - Free for static sites
- **Firebase Hosting** - Free tier

### Database:
- **Neon.tech** ✅ (already using - FREE 512MB)
- **Supabase** - PostgreSQL + free tier
- **PlanetScale** - MySQL, generous free tier

---

## **Testing Your Deployment** ✅

### Test Backend:
```bash
# Check health
curl https://health-harbor-backend.onrender.com/api/storm-watch/

# Test prediction
curl -X POST https://health-harbor-backend.onrender.com/api/storm-watch/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 30, "bmi": 22, "stress_level": 3}'
```

### Test Frontend:
1. Open your Vercel URL: `https://health-harbor-yourname.vercel.app`
2. Check browser console for errors (F12)
3. Test all modules
4. Check Network tab to verify API calls

---

## **Cost Breakdown** 💰

| Service | Free Tier Limits | Cost |
|---------|-----------------|------|
| **Render** | 750 hours/month | **FREE** |
| **Vercel** | 100GB bandwidth/month | **FREE** |
| **Neon** | 512MB storage, 1 project | **FREE** |
| **Gemini API** | 60 requests/minute | **FREE** |
| **GitHub** | Unlimited public repos | **FREE** |
| **Total** | | **$0/month** ✅ |

---

## **Monitoring & Maintenance** 📊

### Render Dashboard:
- View logs: `Dashboard → Services → Logs`
- Monitor usage: Check metrics
- Restart service if needed

### Vercel Dashboard:
- View deployments
- Check analytics
- Monitor bandwidth usage

### Database (Neon):
- [Console](https://console.neon.tech/)
- Monitor storage usage
- Run SQL queries

---

## **Common Issues & Solutions** 🔧

### Backend won't start:
- Check Render logs
- Verify all environment variables are set
- Ensure `gunicorn` is in requirements.txt ✅

### Frontend can't connect to backend:
- Verify `VITE_API_BASE_URL` in Vercel
- Check CORS settings in backend
- Inspect Network tab in browser

### Database connection errors:
- Verify `DATABASE_URL` in Render
- Check Neon database is active
- Ensure IP whitelisting (Neon usually allows all)

### File uploads not working:
- Render has ephemeral file system
- Solution: Use **Cloudinary** for file uploads (free tier)

---

## **Next Steps** 🎯

1. ✅ Set up custom domain (optional)
2. ✅ Enable HTTPS (automatic on Render & Vercel)
3. ✅ Add monitoring (Sentry - free tier)
4. ✅ Set up CI/CD (auto-deploy on git push)
5. ✅ Add caching for better performance

---

## **Quick Deploy Commands Summary** 📝

```bash
# 1. Prepare project
cd "d:\hackthon\Health-Harbor-main (2)\Health-Harbor-main"
git init
git add .
git commit -m "Deploy Health Harbor"

# 2. Create GitHub repo and push
git remote add origin https://github.com/YOUR_USERNAME/health-harbor.git
git push -u origin main

# 3. Deploy backend to Render (via dashboard)
# 4. Deploy frontend to Vercel (via dashboard)
# 5. Update environment variables
# 6. Test and enjoy! 🎉
```

---

## **Support & Resources** 📚

- **Render Docs:** https://render.com/docs
- **Vercel Docs:** https://vercel.com/docs
- **Neon Docs:** https://neon.tech/docs
- **Flask Deployment:** https://flask.palletsprojects.com/en/stable/deploying/

---

**Your Health Harbor app is now live and accessible to the world!** 🌍⚓

**Estimated deployment time:** 15-20 minutes total
