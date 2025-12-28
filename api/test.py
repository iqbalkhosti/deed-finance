"""
Minimal test handler to verify Vercel Python runtime works.
"""
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def test():
    return jsonify({"status": "test_handler_working", "message": "Minimal handler is functional"}), 200

handler = app

