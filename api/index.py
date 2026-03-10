"""
Vercel serverless function entry point.
Exposes the Flask app for Vercel's Python runtime (@vercel/python).

Triple-layered error handling:
  1. Try importing the real Flask app
  2. If that fails, show the error via a minimal Flask app
  3. If Flask itself can't be imported, use a raw WSGI handler
"""
import sys
import os
import traceback

# Add the project root to the path so 'from app import app' works
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Log startup diagnostics to stderr (visible in Vercel function logs)
print(f"[vercel-init] Python {sys.version}", file=sys.stderr)
print(f"[vercel-init] parent_dir={parent_dir}", file=sys.stderr)
print(f"[vercel-init] cwd={os.getcwd()}", file=sys.stderr)
print(f"[vercel-init] DATABASE_URL set: {bool(os.environ.get('DATABASE_URL'))}", file=sys.stderr)

# ---------- Layer 1: Try loading the real app ----------
_import_error = None
app = None

try:
    from app import app as _app
    app = _app
    print("[vercel-init] Flask app imported successfully", file=sys.stderr)
except Exception as e:
    _import_error = {
        "error": str(e),
        "type": type(e).__name__,
        "traceback": traceback.format_exc(),
    }
    print(f"[vercel-init] App import FAILED: {e}", file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)

# ---------- Layer 2: Flask fallback ----------
if app is None:
    try:
        from flask import Flask, jsonify

        _fallback = Flask(__name__)
        _fallback.config["SECRET_KEY"] = "debug"

        @_fallback.route("/", defaults={"path": ""})
        @_fallback.route("/<path:path>")
        def _show_error(path):
            return jsonify(_import_error), 500

        app = _fallback
        print("[vercel-init] Using Flask fallback error handler", file=sys.stderr)
    except Exception as flask_err:
        print(f"[vercel-init] Flask fallback ALSO failed: {flask_err}", file=sys.stderr)

# ---------- Layer 3: Raw WSGI fallback ----------
if app is None:
    import json

    def app(environ, start_response):
        """Bare WSGI handler — last resort when Flask itself won't import."""
        body = json.dumps(
            {
                "error": "App failed to load and Flask fallback also failed",
                "import_error": _import_error,
                "python": sys.version,
            },
            indent=2,
        ).encode()
        start_response(
            "500 Internal Server Error",
            [("Content-Type", "application/json"), ("Content-Length", str(len(body)))],
        )
        return [body]

    print("[vercel-init] Using raw WSGI fallback", file=sys.stderr)

# Vercel's @vercel/python runtime auto-detects a WSGI app named 'app'
