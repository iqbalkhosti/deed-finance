# Vercel Deployment Guide

## Issues Fixed

### 1. **Handler Export** ✅
- Fixed `api/index.py` to properly export the Flask app as `handler` for Vercel's Python runtime

### 2. **Database Path** ✅
- Updated `app.py` to detect Vercel environment and use `/tmp` directory for SQLite database
- Added automatic table initialization on app startup

### 3. **Flask-Mail Initialization** ✅
- Properly initialized Flask-Mail with the app
- Added email configuration from environment variables

### 4. **Static Files** ✅
- Configured `vercel.json` to properly serve static files

## ⚠️ CRITICAL: SQLite Limitation on Vercel

**SQLite on Vercel will NOT persist data** because:
- The `/tmp` directory is cleared between function invocations
- Each serverless function instance has its own isolated filesystem
- Data will be lost when the function goes cold

### Recommended Solutions

#### Option 1: Vercel Postgres (Recommended)
1. Add Vercel Postgres to your project in the Vercel dashboard
2. Update `app.py` to use the Postgres connection string:
   ```python
   import os
   database_url = os.environ.get("POSTGRES_URL")
   if not database_url:
       # Fallback to SQLite for local dev
       database_url = "sqlite:///clients.db"
   engine = create_engine(database_url, echo=False)
   ```

#### Option 2: External Database Service
- Use services like:
  - **Supabase** (free tier available)
  - **PlanetScale** (MySQL)
  - **Railway** (PostgreSQL)
  - **Neon** (PostgreSQL)

#### Option 3: Keep SQLite for Development Only
- Use SQLite locally
- Use a cloud database for production

## Environment Variables

Set these in your Vercel project settings:

### Required
- `SECRET_KEY` - Flask secret key for sessions (generate a strong random string)

### Optional (for email)
- `MAIL_SERVER` - SMTP server (default: smtp.gmail.com)
- `MAIL_PORT` - SMTP port (default: 587)
- `MAIL_USE_TLS` - Use TLS (default: true)
- `MAIL_USERNAME` - Your email username
- `MAIL_PASSWORD` - Your email password
- `MAIL_DEFAULT_SENDER` - Default sender email
- `DEV_MODE` - Set to "false" in production to enable email sending

### For Database (if using Vercel Postgres)
- `POSTGRES_URL` - Automatically provided by Vercel when you add Postgres

## Deployment Steps

1. **Push your code to GitHub/GitLab/Bitbucket**

2. **Connect your repository to Vercel**

3. **Set environment variables** in Vercel dashboard:
   - Go to Project Settings → Environment Variables
   - Add `SECRET_KEY` and other required variables

4. **Deploy**
   - Vercel will automatically detect the Python project
   - The build should complete successfully

5. **Initialize Database** (if using SQLite temporarily):
   - The tables will be created automatically on first request
   - **Note**: Data will be lost when functions go cold

6. **Seed Data** (if needed):
   - You may need to create a one-time script or API endpoint to seed initial data
   - Or run seed_data.py locally and migrate to a persistent database

## Testing the Deployment

After deployment, test these endpoints:
- `/` - Landing page
- `/signup` - User registration
- `/login` - User login
- `/dashboard` - Protected dashboard (requires login)

## Troubleshooting

### Error: FUNCTION_INVOCATION_FAILED
- Check Vercel function logs in the dashboard
- Ensure all environment variables are set
- Verify database connection (if using external DB)

### Error: Database locked / Permission denied
- This is expected with SQLite on Vercel
- Switch to a cloud database solution

### Error: Module not found
- Ensure all dependencies are in `requirements.txt`
- Check that `@vercel/python` is being used in `vercel.json`

## Next Steps

1. **Migrate to Vercel Postgres or another cloud database**
2. **Set up proper email service** (SendGrid, Mailgun, etc.)
3. **Add error monitoring** (Sentry, etc.)
4. **Set up CI/CD** for automated deployments

