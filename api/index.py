"""
Vercel serverless function entry point.
Exposes the Flask app for Vercel's Python runtime (@vercel/python).
"""
import sys
import os

# Add the project root to the path so 'from app import app' works
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Change working directory to project root so relative paths work
os.chdir(parent_dir)

from app import app

# Vercel's @vercel/python runtime auto-detects a WSGI app named 'app'
# No need for 'handler' — 'app' is the standard export name
