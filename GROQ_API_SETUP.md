# 🤖 Groq AI API Setup Guide

## Why Groq?

✅ **100% FREE** - No credit card required  
✅ **14,400 requests/day** - Very generous free tier  
✅ **Extremely fast** - Fastest AI inference available  
✅ **Powerful models** - Llama 3.1 70B, Mixtral, Gemma  
✅ **Easy to use** - OpenAI-compatible API  

---

## 🚀 Quick Setup (5 minutes)

### Step 1: Get Your Free API Key

1. Go to: **https://console.groq.com**
2. Click **"Sign Up"** (use Google/GitHub or email)
3. Once logged in, go to **"API Keys"**
4. Click **"Create API Key"**
5. Copy your API key (starts with `gsk_...`)

### Step 2: Add to Your Project

1. Open `.env` file in your project folder
2. Add this line:
   ```
   GROQ_API_KEY=gsk_your_actual_api_key_here
   ```
3. Save the file

### Step 3: Test It!

Run this command to test:
```powershell
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" -c "from ai_assistant import AIAssistant; ai = AIAssistant(); print('✓ AI Ready!' if ai.api_key else '✗ Add GROQ_API_KEY to .env')"
```

---

## 🎯 What AI Features You Get

### 1. **AI-Powered Cover Letters**
- Personalized for each job
- Professional French writing
- Adapts to your profile
- 250 words, perfect length

### 2. **Smart Job Matching**
- AI analyzes job compatibility
- Gives match score (0-100)
- Lists your strengths
- Suggests improvements

### 3. **Interview Question Generator**
- 10 custom questions per job
- Based on job description
- Company-specific
- Practice-ready

### 4. **Profile Optimizer**
- Analyzes multiple job postings
- Suggests keywords to add
- Recommends skills to learn
- Certification suggestions

---

## 📊 Free Tier Limits

| Feature | Limit |
|---------|-------|
| Requests/Day | 14,400 |
| Requests/Minute | 30 |
| Tokens/Request | 6,000 |
| Models | All (Llama 3.1, Mixtral, etc.) |

**This is MORE than enough for:**
- 100+ cover letters/day
- 500+ job matches/day
- Unlimited profile analysis

---

## 🔧 How to Use in Your App

### Generate Cover Letter
```python
from ai_assistant import AIAssistant
from job_database import JobDatabase
from config import PROFILE

ai = AIAssistant()
db = JobDatabase()
jobs = db.get_new_jobs()

if jobs:
    letter = ai.generate_cover_letter(jobs[0], PROFILE)
    print(letter)
```

### Analyze Job Match
```python
match = ai.analyze_job_match(jobs[0], PROFILE)
print(f"Match Score: {match['score']}%")
print(f"Strengths: {match['strengths']}")
```

### Generate Interview Questions
```python
questions = ai.generate_interview_questions(jobs[0])
for i, q in enumerate(questions, 1):
    print(f"{i}. {q}")
```

---

## ⚡ Alternative Free AI APIs

If you want to try others:

### Google Gemini (Also Free)
```bash
# Get key at: https://ai.google.dev
GEMINI_API_KEY=your_key_here
```

### Hugging Face
```bash
# Get key at: https://huggingface.co/settings/tokens
HF_API_KEY=your_key_here
```

---

## 🆘 Troubleshooting

**Problem:** "AI API Error"
- **Solution:** Check your API key in `.env` file
- Make sure it starts with `gsk_`
- No spaces before/after the key

**Problem:** "Rate limit exceeded"
- **Solution:** You've used 14,400 requests today
- Wait until tomorrow or create another account

**Problem:** "No response from AI"
- **Solution:** Check internet connection
- Groq servers might be down (rare)
- Fallback responses will be used automatically

---

## 💡 Pro Tips

1. **Test First:** Always test with one job before bulk operations
2. **Save Responses:** AI responses are cached to save API calls
3. **Fallback Works:** If AI fails, template responses are used
4. **Monitor Usage:** Check https://console.groq.com for usage stats

---

## 🎉 You're All Set!

Once you add your API key, the AI features will automatically activate in:
- ✅ Cover letter generation
- ✅ Job matching analysis
- ✅ Interview preparation
- ✅ Profile optimization

**No code changes needed - it just works!** 🚀
