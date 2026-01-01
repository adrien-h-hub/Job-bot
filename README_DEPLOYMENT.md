# 🚀 Stage & Alternance Finder - Deployment Guide

## ✅ All Files Updated & Ready for Deployment!

---

## 📦 What's Been Updated

### 1. **Procfile** ✅
```
web: gunicorn web_dashboard:app
```
- Correctly references Flask app
- Uses Gunicorn for production

### 2. **requirements.txt** ✅
- All dependencies listed
- Compatible with Python 3.11
- Includes Flask, Gunicorn, etc.

### 3. **render.yaml** ✅
```yaml
services:
  - type: web
    name: stage-alternance-finder
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn web_dashboard:app
```
- Auto-configuration for Render
- Environment variables set up

### 4. **web_dashboard.py** ✅
- Port configuration added for deployment
- Debug mode disabled for production
- All routes working

### 5. **.gitignore** ✅
- Excludes sensitive files (.env)
- Excludes database files
- Clean deployment

---

## 🎯 RECOMMENDED: Deploy to Render.com (FREE)

### Why Render?
- ✅ **100% FREE** - No credit card
- ✅ **5 minutes** to deploy
- ✅ **Auto-deploy** from GitHub
- ✅ **SSL included** (HTTPS)
- ✅ **Your files are ready!**

---

## 🚀 Deployment Steps (5 Minutes)

### Option A: Deploy from GitHub (Recommended)

#### Step 1: Push to GitHub
```bash
# Navigate to your project
cd c:\Users\Dardq\CascadeProjects\commen_skip_GE\job_hunter_bot

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Stage & Alternance Finder - Ready for deployment"

# Create GitHub repo and push
# (Create repo at github.com first)
git remote add origin https://github.com/YOUR_USERNAME/stage-alternance-finder.git
git branch -M main
git push -u origin main
```

#### Step 2: Deploy on Render
1. Go to: **https://render.com**
2. Click **"Get Started for Free"**
3. Sign up with GitHub (easiest)
4. Click **"New +"** → **"Web Service"**
5. Click **"Connect GitHub"**
6. Select your repository: `stage-alternance-finder`
7. Render auto-detects settings from `render.yaml`
8. Click **"Create Web Service"**
9. Wait 3-5 minutes for deployment
10. Done! 🎉

#### Step 3: Get Your URL
- Render provides: `https://stage-alternance-finder.onrender.com`
- Or custom subdomain: `https://YOUR-NAME.onrender.com`

---

### Option B: Deploy to Railway.app

1. Go to: **https://railway.app**
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub"**
4. Select your repo
5. Railway auto-detects Flask
6. Get URL: `https://your-app.railway.app`

**Free Tier:** $5 credits/month

---

### Option C: Deploy to PythonAnywhere

1. Go to: **https://www.pythonanywhere.com**
2. Sign up for free account
3. Upload files via web interface
4. Configure WSGI file
5. Get URL: `https://yourusername.pythonanywhere.com`

**Free Tier:** Always free, but slower

---

## 🧪 After Deployment - Test All Features

Once deployed, test these:

### 1. **Login System** ✅
- URL: `https://your-app-url.com`
- Username: `admin`
- Password: `admin123`

### 2. **Onboarding Questionnaire** ✅
- Should appear after login
- 6 questions about preferences
- Submit and save

### 3. **Dashboard** ✅
- View stats cards
- Purple gradient background
- Navigation menu works

### 4. **Jobs Page** ✅
- Browse stages & alternances
- Job cards display correctly
- Navigation between pages

### 5. **Profile Page** ✅
- Profile optimization
- Missing keywords
- Suggestions

### 6. **Career Plan** ✅
- Career development plan
- Skill gaps
- Milestones

### 7. **Navigation Menu** ✅
- 4 tabs (Dashboard, Jobs, Profile, Career)
- Smooth transitions
- Active indicator animation

---

## 🔧 Environment Variables (Optional)

Add these in Render dashboard if you want AI features:

```
GROQ_API_KEY=gsk_your_key_here
```

Get free key at: https://console.groq.com

---

## 📊 Free Tier Limits

### Render.com:
- ✅ 750 hours/month
- ✅ Persistent storage
- ✅ SSL certificate
- ⚠️ Sleeps after 15 min inactivity

### Railway.app:
- ✅ $5 credits/month
- ✅ No sleep
- ✅ Fast performance

### PythonAnywhere:
- ✅ Always free
- ✅ No sleep
- ⚠️ Slower performance

---

## 🆘 Troubleshooting

### Deployment fails?
1. Check Render logs in dashboard
2. Verify `requirements.txt` has all dependencies
3. Check Python version (should be 3.11)
4. Verify `Procfile` is correct

### App crashes?
1. Check Render logs for errors
2. Verify environment variables
3. Check database permissions

### Can't login?
1. Clear browser cache
2. Try different browser
3. Check if app is fully deployed

---

## 🎉 You're Ready!

All files are updated and ready for deployment. Choose your platform:

1. **Render.com** ⭐ (Recommended) - https://render.com
2. **Railway.app** - https://railway.app
3. **PythonAnywhere** - https://www.pythonanywhere.com

**Deployment time:** 5 minutes  
**Your app will be live!** 🚀

---

## 📞 Need Help?

If you encounter issues:
1. Check deployment logs
2. Verify all files are uploaded
3. Check environment variables
4. Review this guide

**Good luck with your deployment!** 🎯
