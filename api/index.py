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
Minimal handler to avoid Vercel runtime scanning issues.
"""
import sys
import os

# Setup path
_parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _parent not in sys.path:
    sys.path.insert(0, _parent)

# Import app - this will load all modules
# Vercel's runtime scans AFTER this import, so we need to ensure
# Base is not accessible from the app module's namespace
try:
    from app import app as _flask_app
    print("DEBUG: App imported successfully")
except Exception as e:
    print(f"DEBUG ERROR: {type(e).__name__}: {str(e)}")
    from flask import Flask, jsonify
    _flask_app = Flask(__name__)
    @_flask_app.route("/", defaults={"path": ""})
    @_flask_app.route("/<path:path>")
    def _err(path):
        return jsonify({"error": str(e), "type": type(e).__name__}), 500

# Export handler - Vercel expects this
handler = _flask_app

# Clean up - remove all temporary variables
# This ensures Vercel's scanner only sees 'handler'
for _name in list(globals().keys()):
    if _name not in ('handler', '__name__', '__doc__', '__file__', '__package__', '__loader__', '__spec__'):
        if not _name.startswith('__'):
            try:
                del globals()[_name]
            except:
                pass

print("DEBUG: Handler ready")
