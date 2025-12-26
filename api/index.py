"""
Vercel serverless function entry point.
This file exposes the Flask app for Vercel's Python runtime.
"""
import sys
import os

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel expects the app to be named 'app' or 'handler'
# The @vercel/python runtime will automatically use this
