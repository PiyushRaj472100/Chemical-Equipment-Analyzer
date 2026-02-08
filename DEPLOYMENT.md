# Deployment Guide

## Backend Deployment (Render)

### Prerequisites
- Render account (free tier available)
- GitHub repository connected

### Steps

1. **Push your code to GitHub** (already done)

2. **Create a new Web Service on Render**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `Chemical-Equipment-Analyzer` repo

3. **Configure the Web Service**
   - **Name**: `chemical-equipment-analyzer-api`
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn chemical_analyzer.wsgi:application`
   - **Instance Type**: Free

4. **Add Environment Variables**
   - `SECRET_KEY`: Generate a random secret key
   - `DEBUG`: `false`
   - `ALLOWED_HOSTS`: `.onrender.com`
   - `DATABASE_URL`: (Render will automatically add this for PostgreSQL)

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Note your API URL: `https://your-app-name.onrender.com`

## Frontend Deployment (Vercel)

### Prerequisites
- Vercel account (free tier available)
- GitHub repository connected

### Steps

1. **Create a new Project on Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Select the `Chemical-Equipment-Analyzer` repo

2. **Configure the Project**
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend-web`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

3. **Add Environment Variables**
   - `REACT_APP_API_URL`: `https://your-backend-url.onrender.com/api`
   - (Replace with your actual Render URL)

4. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete
   - Note your frontend URL: `https://your-app-name.vercel.app`

## Post-Deployment Configuration

### Update Backend CORS Settings

After getting your Vercel URL, update the backend CORS settings:

1. Go to your Render dashboard
2. Add environment variable:
   - `CORS_ALLOWED_ORIGINS`: `https://your-vercel-app.vercel.app`
3. Redeploy the backend

### Test the Deployment

1. Visit your Vercel frontend URL
2. Try registering a new user
3. Login with the registered credentials
4. Upload a CSV file
5. Check if all features work correctly

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Make sure the backend CORS settings include your Vercel URL
   - Check that `CORS_ALLOW_CREDENTIALS` is set to `True`

2. **Database Connection Issues**
   - Ensure the `DATABASE_URL` environment variable is set
   - Run migrations if needed

3. **Build Failures**
   - Check that all dependencies are in requirements.txt
   - Verify the build and start commands are correct

4. **API Connection Issues**
   - Verify the `REACT_APP_API_URL` is correct
   - Check that the backend is running and accessible

### Environment Variables Reference

**Backend (Render)**:
```
SECRET_KEY=your-secret-key-here
DEBUG=false
ALLOWED_HOSTS=.onrender.com
CORS_ALLOWED_ORIGINS=https://your-vercel-app.vercel.app
```

**Frontend (Vercel)**:
```
REACT_APP_API_URL=https://your-backend-app.onrender.com/api
```

## Local Development

To continue local development:

1. Create `.env` file in `frontend-web/`:
   ```
   REACT_APP_API_URL=http://localhost:8000/api
   ```

2. Run backend: `python manage.py runserver`
3. Run frontend: `npm start`

## URLs After Deployment

- **Backend API**: `https://your-app-name.onrender.com/api`
- **Frontend**: `https://your-app-name.vercel.app`
- **API Endpoints**:
  - Register: `POST /api/register/`
  - Login: `POST /api/login/`
  - Upload: `POST /api/upload/`
  - History: `GET /api/history/`
  - PDF: `GET /api/generate-pdf/{id}/`
