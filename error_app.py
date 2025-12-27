import traceback
from flask import Flask, jsonify

try:
    # Change "app" to whatever your main file is actually named
    # If your Flask instance file is main.py, use: from main import app
    from app import app  # <-- adjust if needed

except Exception as e:
    error_app = Flask(__name__)

    @error_app.route("/", defaults={"path": ""})
    @error_app.route("/<path:path>")
    def show_error(path):
        return jsonify({
            "error": "Flask app failed to import / initialize",
            "exception_type": type(e).__name__,
            "message": str(e),
            "traceback": traceback.format_exc(),
            "path": path
        }), 500

    app = error_app  # <-- IMPORTANT: export as "app"
