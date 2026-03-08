"""
Minimal test — zero project imports.
If this crashes, the issue is with pip install / Vercel config.
If this works, the issue is with one of our dependencies.
"""
from flask import Flask, jsonify
import sys

app = Flask(__name__)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def hello(path):
    return jsonify({
        "status": "alive",
        "python": sys.version,
        "message": "Minimal test works! The issue is with a project dependency."
    })
