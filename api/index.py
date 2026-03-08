"""
Vercel serverless function entry point — DIAGNOSTIC MODE.
Tests each import individually to find which dependency crashes the process.
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

# ── Diagnostic: test each import individually ──
_diag = {}

_test_imports = [
    ("flask", "from flask import Flask"),
    ("sqlalchemy", "import sqlalchemy"),
    ("pg8000", "import pg8000"),
    ("bcrypt", "import bcrypt"),
    ("flask_bcrypt", "from flask_bcrypt import Bcrypt"),
    ("flask_login", "import flask_login"),
    ("flask_wtf", "import flask_wtf"),
    ("flask_mail", "import flask_mail"),
    ("dotenv", "from dotenv import load_dotenv"),
    ("anthropic", "import anthropic"),
    ("openai", "import openai"),
    ("email_validator", "import email_validator"),
    ("config", "from config import Config"),
    ("db", "from db import engine, Session"),
    ("models", "from models import DbBase, Client"),
    ("forms", "from forms import SignupForm"),
    ("email_utils", "from email_utils import mail"),
    ("app", "from app import app as _app"),
]

for name, stmt in _test_imports:
    try:
        exec(stmt)
        _diag[name] = "ok"
    except Exception as e:
        _diag[name] = f"FAIL: {type(e).__name__}: {e}"
        # Stop after first failure in chain deps
        if name in ("flask",):
            break

# ── Build a diagnostic app (or use the real one if it loaded) ──
_import_error = None

if "app" in _diag and _diag["app"] == "ok":
    # Real app loaded successfully
    from app import app as _real_app
    app = _real_app
else:
    # Show diagnostic results
    from flask import Flask, jsonify
    _fallback = Flask(__name__)
    _fallback.config["SECRET_KEY"] = "debug"

    @_fallback.route("/", defaults={"path": ""})
    @_fallback.route("/<path:path>")
    def _show_diag(path):
        return jsonify({
            "status": "diagnostic",
            "imports": _diag,
            "python_version": sys.version,
            "platform": sys.platform,
        }), 500

    app = _fallback
