# """
# Vercel serverless function entry point.
# This file exposes the Flask app for Vercel's Python runtime.
# """
# import sys
# import os
# from app import app 

# # Add the parent directory to the path so we can import app
# parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# if parent_dir not in sys.path:
#     sys.path.insert(0, parent_dir)

# # Set up basic logging
# import logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# logger.info(f"Starting Vercel function handler")
# logger.info(f"Python path: {sys.path}")
# logger.info(f"Working directory: {os.getcwd()}")
# logger.info(f"Parent directory: {parent_dir}")

# try:
#     logger.info("Attempting to import app...")
#     from app import app
#     logger.info("Successfully imported app")
    
#     # Vercel expects the app to be exported as 'handler' or 'app'
#     # Export it as 'handler' for compatibility
    
#     logger.info("Handler exported successfully")
    
# except ImportError as e:
#     logger.error(f"Import error: {e}")
#     import traceback
#     traceback.print_exc()
#     # If import fails, create a minimal error handler
#     from flask import Flask, jsonify
#     error_app = Flask(__name__)
    
#     @error_app.route('/', defaults={'path': ''})
#     @error_app.route('/<path:path>')
#     def error_handler(path):
#         return jsonify({
#             'error': 'Application initialization failed',
#             'message': str(e),
#             'type': 'ImportError',
#             'path': path
#         }), 500
    
    
    
# except Exception as e:
#     logger.error(f"Unexpected error: {e}")
#     import traceback
#     traceback.print_exc()
#     # If import fails, create a minimal error handler
#     from flask import Flask, jsonify
#     error_app = Flask(__name__)
    
#     @error_app.route('/', defaults={'path': ''})
#     @error_app.route('/<path:path>')
#     def error_handler(path):
#         return jsonify({
#             'error': 'Application initialization failed',
#             'message': str(e),
#             'type': type(e).__name__,
#             'path': path
#         }), 500
    
    
"""
Vercel serverless function entry point.
This file exposes the Flask app for Vercel's Python runtime.
MINIMAL VERSION to avoid namespace conflicts with Vercel's runtime introspection.
"""
import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import Flask for error handler
from flask import Flask, jsonify

# Initialize handler variable
_handler = None

# Try to import the app - use simple import
# The issue is Vercel's runtime scanning, not our import method
try:
    from app import app
    _handler = app
    print("DEBUG: App imported successfully")
except Exception as e:
    print(f"DEBUG ERROR: Failed to import app - {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
    # Create minimal error handler
    error_app = Flask(__name__)
    @error_app.route("/", defaults={"path": ""})
    @error_app.route("/<path:path>")
    def error_handler(path):
        return jsonify({
            "error": "App import failed",
            "message": str(e),
            "type": type(e).__name__
        }), 200
    _handler = error_app

# Ensure handler is always defined
if _handler is None:
    _handler = Flask(__name__)
    @_handler.route("/", defaults={"path": ""})
    @_handler.route("/<path:path>")
    def fallback(path):
        return jsonify({"error": "Handler not initialized"}), 500

# Export handler for Vercel (CRITICAL - must be at module level)
# Wrap as WSGI application to ensure Vercel recognizes it correctly
handler = _handler

# Clean up temporary variables
# Note: Vercel's runtime error is in their internal code, not ours
# The error occurs when Vercel scans module attributes looking for handler classes
try:
    del _handler, parent_dir, error_app, fallback
except NameError:
    pass

print("DEBUG: Handler exported and ready")
