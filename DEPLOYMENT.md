# 🚀 Deployment Guide

This guide covers deploying the Plivo AI Playground to various hosting platforms.

## 📱 Vercel Deployment (Frontend)

### Prerequisites
- GitHub account
- Vercel account (free tier available)
- Repository pushed to GitHub

### Steps

1. **Connect Repository to Vercel**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your GitHub repository
   - Select the `frontend` folder as the root directory

2. **Configure Build Settings**
   - Framework Preset: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

3. **Set Environment Variables**
   ```
   VITE_API_BASE_URL=https://your-backend-url.com/api/v1
   VITE_APP_NAME=Plivo AI Playground
   VITE_CLERK_PUBLISHABLE_KEY=your_clerk_key (optional)
   ```

4. **Deploy**
   - Click "Deploy"
   - Your frontend will be available at `https://your-project.vercel.app`

## 🐍 Railway Deployment (Backend)

### Prerequisites
- GitHub account
- Railway account (free tier available)

### Steps

1. **Connect Repository to Railway**
   - Go to [Railway Dashboard](https://railway.app/dashboard)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

2. **Configure Service**
   - Set root directory to `backend`
   - Railway will auto-detect Python and install dependencies

3. **Set Environment Variables**
   ```
   PORT=5001
   FRONTEND_URL=https://your-frontend.vercel.app
   GEMINI_API_KEY=your_gemini_api_key
   GOOGLE_API_KEY=your_google_api_key
   ```

4. **Configure Startup**
   - Railway should auto-detect `python main.py`
   - If not, set start command: `python main.py`

5. **Deploy**
   - Railway will provide a URL like `https://your-backend.railway.app`
   - Update your frontend `VITE_API_BASE_URL` to this URL

## 🔄 Alternative Backend Hosting

### Render
1. Connect GitHub repository
2. Select "Web Service"
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python main.py`
5. Add environment variables

### Heroku
1. Create new app on Heroku
2. Connect GitHub repository
3. Add Python buildpack
4. Set environment variables
5. Deploy from GitHub

### DigitalOcean App Platform
1. Create new app
2. Connect GitHub repository
3. Configure Python service
4. Set environment variables
5. Deploy

## 🌐 Custom Domain Setup

### Vercel Custom Domain
1. Go to your project settings
2. Click "Domains"
3. Add your custom domain
4. Configure DNS records as instructed

### Railway Custom Domain
1. Go to your service settings
2. Click "Settings" → "Domains"
3. Add custom domain
4. Configure DNS records

## 📊 Environment Variables Reference

### Frontend (.env)
```env
VITE_API_BASE_URL=https://your-backend.railway.app/api/v1
VITE_APP_NAME=Plivo AI Playground
VITE_CLERK_PUBLISHABLE_KEY=pk_test_... (optional)
```

### Backend (.env)
```env
PORT=5001
FRONTEND_URL=https://your-frontend.vercel.app
GEMINI_API_KEY=AIzaSy...
GOOGLE_API_KEY=AIzaSy...
OPENAI_API_KEY=sk-proj-... (optional)
ASSEMBLYAI_API_KEY=... (optional)
```

## 🔧 Post-Deployment Checklist

- [ ] Frontend loads without errors
- [ ] Backend API responds at `/docs` endpoint
- [ ] CORS is configured correctly
- [ ] All API endpoints work
- [ ] File uploads function properly
- [ ] Environment variables are set
- [ ] Custom domain configured (if applicable)

## 🐛 Common Deployment Issues

### CORS Errors
- Ensure `FRONTEND_URL` in backend matches your frontend domain
- Check CORS middleware configuration

### API Connection Failed
- Verify `VITE_API_BASE_URL` points to correct backend
- Ensure backend is running and accessible

### Environment Variables Not Loading
- Double-check variable names (case-sensitive)
- Ensure all required variables are set
- For frontend: variables must start with `VITE_`

### Build Failures
- Check build logs for specific errors
- Ensure all dependencies are listed correctly
- Verify Python/Node versions

## 📈 Performance Optimization

### Frontend
- Enable Vercel analytics
- Use Vercel Image Optimization
- Configure caching headers

### Backend
- Use production ASGI server (Gunicorn + Uvicorn)
- Configure request timeouts
- Add rate limiting
- Use CDN for static files

## 🔒 Security Considerations

### API Keys
- Never commit `.env` files
- Use platform environment variables
- Rotate keys regularly

### CORS
- Set specific frontend domains (not `*`)
- Use HTTPS in production
- Validate file uploads

### Headers
- Add security headers
- Enable HTTPS redirect
- Configure CSP headers

---

Need help with deployment? Check the main README.md or create an issue in the repository.
