"""
Dependency test phase 2 — try importing the full app module.
All individual deps work, so the crash is in app.py initialization.
"""
import sys
import os
import traceback

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
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

# If import failed, show the actual error
if app is None:
    from flask import Flask, jsonify
    _fallback = Flask(__name__)
    _fallback.config["SECRET_KEY"] = "debug"

    @_fallback.route("/", defaults={"path": ""})
    @_fallback.route("/<path:path>")
    def _show_error(path):
        return jsonify({
            "status": "app_import_failed",
            "error": _import_error,
        }), 500

    app = _fallback
