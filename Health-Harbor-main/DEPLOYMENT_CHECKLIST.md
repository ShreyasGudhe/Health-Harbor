# 📋 Health Harbor Deployment Checklist

Use this checklist to ensure smooth deployment.

---

## **Pre-Deployment** ✅

### Code Preparation
- [ ] Update `requirements.txt` with gunicorn ✅ (Done)
- [ ] Configure CORS for production ✅ (Done)
- [ ] Remove hardcoded URLs
- [ ] Test locally (backend on 5000, frontend on 3000)
- [ ] Check all environment variables are in `.env.example`

### Git Repository
- [ ] Initialize git repository
- [ ] Verify `.gitignore` excludes sensitive files
- [ ] Commit all code
- [ ] Create GitHub repository
- [ ] Push to GitHub

### Environment Variables to Set
- [ ] `SECRET_KEY` - Generate random secret
- [ ] `DATABASE_URL` - Copy from local .env
- [ ] `GEMINI_API_KEY` - Copy from local .env  
- [ ] `FLASK_DEBUG` - Set to `False`
- [ ] `CAPTAINS_LOG_TABLE_NAME` - Set to `captains_log_entries`

---

## **Backend Deployment (Render)** 🔧

- [ ] Sign up for [Render.com](https://render.com/)
- [ ] Create new Web Service
- [ ] Connect GitHub repository
- [ ] Set root directory: `vitalplunder/backend`
- [ ] Configure build command:
  ```bash
  pip install -r requirements.txt && python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('vader_lexicon'); nltk.download('brown')"
  ```
- [ ] Configure start command:
  ```bash
  gunicorn -b 0.0.0.0:$PORT app:create_app()
  ```
- [ ] Add all environment variables
- [ ] Wait for deployment to complete (5-10 min)
- [ ] Test backend endpoint: `https://your-app.onrender.com/api/storm-watch/`
- [ ] Copy backend URL for frontend configuration

---

## **Frontend Deployment (Vercel)** 🌐

- [ ] Sign up for [Vercel.com](https://vercel.com/)
- [ ] Import GitHub repository
- [ ] Set framework preset: `Vite`
- [ ] Set root directory: `vitalplunder/frontend`
- [ ] Set build command: `npm run build`
- [ ] Set output directory: `dist`
- [ ] Add environment variable:
  ```
  VITE_API_BASE_URL=https://your-backend.onrender.com/api
  ```
- [ ] Deploy and wait (2-3 min)
- [ ] Test frontend: Open Vercel URL
- [ ] Check browser console for errors
- [ ] Test all module features

---

## **Post-Deployment Testing** ✅

### Backend Tests
- [ ] Health check: `GET /api/storm-watch/`
- [ ] Prediction: `POST /api/storm-watch/predict`
- [ ] All modules accessible
- [ ] Database connection working
- [ ] Gemini API working (Ship Doctor)

### Frontend Tests
- [ ] App loads without errors
- [ ] All pages accessible
- [ ] API calls working (check Network tab)
- [ ] Modules render correctly
- [ ] Forms submit successfully

### Integration Tests
- [ ] Storm Watch: Submit health data
- [ ] Mind Compass: Analyze mood
- [ ] Captain's Log: Create journal entry
- [ ] Treasure Ledger: Add transaction
- [ ] Ship Doctor: Upload document (if file storage configured)

---

## **Optional Enhancements** 🚀

- [ ] Configure custom domain
- [ ] Set up monitoring (Sentry)
- [ ] Add analytics (Google Analytics/Plausible)
- [ ] Configure file storage (Cloudinary for uploads)
- [ ] Set up automated backups for database
- [ ] Add CI/CD pipeline
- [ ] Configure alerts for errors
- [ ] Add rate limiting
- [ ] Set up caching (Redis)

---

## **Monitoring & Maintenance** 📊

### Weekly
- [ ] Check Render logs for errors
- [ ] Monitor Vercel analytics
- [ ] Check database storage usage (Neon dashboard)
- [ ] Verify all services are running

### Monthly
- [ ] Review Render free tier usage (750 hours)
- [ ] Check Vercel bandwidth usage
- [ ] Update dependencies if needed
- [ ] Review and rotate secrets

---

## **Troubleshooting** 🔧

### Backend not starting?
1. Check Render logs
2. Verify all environment variables are set
3. Test locally first
4. Check Python version (3.11)

### Frontend can't reach backend?
1. Verify `VITE_API_BASE_URL` is correct
2. Check CORS settings in backend
3. Inspect Network tab in browser DevTools
4. Verify backend is running

### Database errors?
1. Check `DATABASE_URL` is correct
2. Verify Neon database is active
3. Check table exists: `captains_log_entries`
4. Review database logs in Neon console

---

## **Important URLs** 🔗

### Services
- Render Dashboard: https://dashboard.render.com/
- Vercel Dashboard: https://vercel.com/dashboard
- Neon Console: https://console.neon.tech/
- GitHub Repo: https://github.com/YOUR_USERNAME/health-harbor

### Deployed Apps
- Backend: https://your-app.onrender.com
- Frontend: https://your-app.vercel.app
- API Docs: https://your-app.onrender.com/api/storm-watch/

---

## **Deployment Complete!** 🎉

Once all items are checked, your Health Harbor app is:
- ✅ Live and accessible worldwide
- ✅ Connected to cloud database
- ✅ Using AI/ML models
- ✅ Running on free tier
- ✅ Auto-deploying on git push

**Total cost: $0/month** 💰

**Deployment time: ~20 minutes** ⏱️

---

*For detailed step-by-step instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)*
