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
    
    
import traceback
from flask import Flask, jsonify

try:
    # IMPORTANT: this must match your main Flask file name
    from app import app   # change to "from main import app" if your file is main.py

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

    app = error_app  # THIS LINE IS CRITICAL
