"""
Dependency test — import suspicious native extensions one by one.
If this crashes, one of these imports has incompatible native code.
"""
from flask import Flask, jsonify
import sys

# ── Test native-extension imports (these are the crash suspects) ──
results = {}

# Test 1: bcrypt (Rust-compiled extension)
try:
    import bcrypt
    results["bcrypt"] = f"ok (v{bcrypt.__version__})"
except Exception as e:
    results["bcrypt"] = f"FAIL: {e}"

# Test 2: SQLAlchemy (uses greenlet C extension)
try:
    import sqlalchemy
    results["sqlalchemy"] = f"ok (v{sqlalchemy.__version__})"
except Exception as e:
    results["sqlalchemy"] = f"FAIL: {e}"

# Test 3: pg8000 (pure Python — should be fine)
try:
    import pg8000
    results["pg8000"] = "ok"
except Exception as e:
    results["pg8000"] = f"FAIL: {e}"

# Test 4: anthropic
try:
    import anthropic
    results["anthropic"] = f"ok (v{anthropic.__version__})"
except Exception as e:
    results["anthropic"] = f"FAIL: {e}"

# Test 5: openai
try:
    import openai
    results["openai"] = f"ok (v{openai.__version__})"
except Exception as e:
    results["openai"] = f"FAIL: {e}"

# Test 6: flask_bcrypt (wraps bcrypt)
try:
    from flask_bcrypt import Bcrypt
    results["flask_bcrypt"] = "ok"
except Exception as e:
    results["flask_bcrypt"] = f"FAIL: {e}"

# Test 7: our db module
try:
    import os
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    os.chdir(parent_dir)
    from db import engine, Session
    results["db_module"] = "ok"
except Exception as e:
    results["db_module"] = f"FAIL: {e}"

# Test 8: our models module
try:
    from models import DbBase, Client
    results["models"] = "ok"
except Exception as e:
    results["models"] = f"FAIL: {e}"

app = Flask(__name__)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def hello(path):
    return jsonify({
        "status": "dependency_test",
        "python": sys.version,
        "results": results,
    })
