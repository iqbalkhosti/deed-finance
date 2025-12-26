# Troubleshooting Vercel Deployment

## Changes Made

### 1. Enhanced Error Handling in `api/index.py`
- Added comprehensive logging to track import process
- Added error handler that catches import failures and returns JSON error responses
- This will help identify if the issue is during import or runtime

### 2. Improved Database Initialization
- Added fallback to in-memory database if file-based database fails
- Better error handling with traceback printing
- Improved Vercel environment detection

### 3. Safer Flask-Mail Initialization
- Wrapped mail initialization in try-except to prevent crashes if email config is missing

### 4. Added Health Check Endpoint
- `/health` endpoint to test if the app is running and database is accessible

## How to Debug

### Step 1: Check Vercel Function Logs
1. Go to your Vercel dashboard
2. Navigate to your project
3. Click on "Functions" tab
4. Look for the function logs - you should now see detailed logging from `api/index.py`
5. Look for errors like:
   - Import errors
   - Database initialization errors
   - Missing module errors

### Step 2: Test the Health Endpoint
After deployment, try accessing:
```
https://your-app.vercel.app/health
```

This will return JSON with:
- Status
- Database path
- Vercel environment detection
- Database connection status

### Step 3: Check Common Issues

#### Issue: Import Error
**Symptoms:** Error in logs shows "ImportError" or "ModuleNotFoundError"
**Solution:** 
- Check that all dependencies are in `requirements.txt`
- Ensure `@vercel/python` is specified in `vercel.json`

#### Issue: Database Error
**Symptoms:** Error mentions "database" or "sqlite"
**Solution:**
- The app now falls back to in-memory database if file-based fails
- For production, migrate to Vercel Postgres (see VERCEL_DEPLOYMENT.md)

#### Issue: Missing Environment Variables
**Symptoms:** Error mentions "SECRET_KEY" or configuration
**Solution:**
- Set `SECRET_KEY` in Vercel environment variables
- Other variables are optional but may be needed for full functionality

#### Issue: Static Files Not Loading
**Symptoms:** CSS/images not loading
**Solution:**
- Check `vercel.json` routes configuration
- Ensure static files are in the `static/` directory

## Next Steps

1. **Deploy the updated code**
2. **Check the function logs** in Vercel dashboard
3. **Visit `/health` endpoint** to see status
4. **Share the logs** if still failing - the enhanced logging should show the exact error

## Expected Log Output

When the function starts, you should see in the logs:
```
Starting Vercel function handler
Python path: [...]
Working directory: [...]
Parent directory: [...]
Attempting to import app...
Database initialized at: /tmp/clients.db (or clients.db)
Successfully imported app
Handler exported successfully
```

If you see errors, they will be logged with full tracebacks.

## If Still Failing

If the app still crashes after these changes:

1. **Copy the full error logs** from Vercel dashboard
2. **Check what the last log message is** - this will tell us where it's failing
3. **Try accessing `/health`** - if this works, the app is running but routes might have issues
4. **Check if it's a specific route** - try accessing just `/` first

The enhanced error handling should now provide much better diagnostics.

