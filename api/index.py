"""
Vercel serverless function entry point.
Exposes the Flask app as a handler for Vercel's Python runtime.
"""
import sys
import os

# Add the project root to the path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from app import app

# Vercel expects 'handler' or 'app' to be exported
handler = app
