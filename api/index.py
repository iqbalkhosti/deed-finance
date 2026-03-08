"""
Vercel serverless function entry point.
Exposes the Flask app for Vercel's Python runtime (@vercel/python).
"""
import sys
import os
import traceback

# Add the project root to the path so 'from app import app' works
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Change working directory to project root so relative paths work
os.chdir(parent_dir)

_import_error = None
app = None

try:
    from app import app as _app
    app = _app
except Exception as e:
    _import_error = {
        "error": str(e),
        "type": type(e).__name__,
        "traceback": traceback.format_exc(),
    }

# If import failed, expose a minimal Flask app that returns the error for debugging
if app is None:
    from flask import Flask, jsonify
    _fallback = Flask(__name__)
    _fallback.config["SECRET_KEY"] = "debug"

    @_fallback.route("/", defaults={"path": ""})
    @_fallback.route("/<path:path>")
    def _show_error(path):
        return jsonify(_import_error), 500

    app = _fallback

# Vercel's @vercel/python runtime auto-detects a WSGI app named 'app'
