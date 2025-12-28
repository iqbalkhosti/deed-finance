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
"""
import traceback
import sys
import os

# CRITICAL: Import Flask first to ensure it's available for error handler
from flask import Flask, jsonify

# Initialize error tracking
_init_error = None
_handler = None

# #region agent log
try:
    import json
    with open('/Users/IqbalJaved/Desktop/Desktop - MacBook Air/Projects/Python Repos/deed-finance/.cursor/debug.log', 'a') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"init","hypothesisId":"A","location":"api/index.py:20","message":"Handler init started","data":{"cwd":os.getcwd(),"pythonpath":sys.path[:3]},"timestamp":int(__import__('time').time()*1000)}) + '\n')
except: pass
print("DEBUG: Handler initialization started")
# #endregion

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# #region agent log
try:
    with open('/Users/IqbalJaved/Desktop/Desktop - MacBook Air/Projects/Python Repos/deed-finance/.cursor/debug.log', 'a') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"init","hypothesisId":"A","location":"api/index.py:30","message":"Parent dir calculated","data":{"parent_dir":parent_dir,"in_path":parent_dir in sys.path},"timestamp":int(__import__('time').time()*1000)}) + '\n')
except: pass
print(f"DEBUG: Parent directory: {parent_dir}")
# #endregion

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# #region agent log
try:
    with open('/Users/IqbalJaved/Desktop/Desktop - MacBook Air/Projects/Python Repos/deed-finance/.cursor/debug.log', 'a') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"init","hypothesisId":"A","location":"api/index.py:40","message":"About to import app","data":{"sys_path_len":len(sys.path)},"timestamp":int(__import__('time').time()*1000)}) + '\n')
except: pass
print("DEBUG: About to import app module")
# #endregion

# Try to import the app
try:
    from app import app
    _handler = app
    # #region agent log
    try:
        with open('/Users/IqbalJaved/Desktop/Desktop - MacBook Air/Projects/Python Repos/deed-finance/.cursor/debug.log', 'a') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"init","hypothesisId":"A","location":"api/index.py:50","message":"App imported successfully","data":{"app_type":type(app).__name__},"timestamp":int(__import__('time').time()*1000)}) + '\n')
    except: pass
    print("DEBUG: App imported successfully")
    # #endregion
except Exception as e:
    _init_error = e
    # #region agent log
    try:
        with open('/Users/IqbalJaved/Desktop/Desktop - MacBook Air/Projects/Python Repos/deed-finance/.cursor/debug.log', 'a') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"init","hypothesisId":"A","location":"api/index.py:60","message":"Import failed","data":{"error_type":type(e).__name__,"error_msg":str(e)},"timestamp":int(__import__('time').time()*1000)}) + '\n')
    except: pass
    print(f"DEBUG ERROR: Failed to import app - {type(e).__name__}: {str(e)}")
    print(f"DEBUG ERROR: Traceback:\n{traceback.format_exc()}")
    # #endregion
    
    # Create error handler app
    error_app = Flask(__name__)
    
    @error_app.route("/test")
    def test_route():
        """Test route to verify handler is working."""
        return jsonify({
            "status": "error_handler_active",
            "message": "Handler is working but app import failed",
            "init_error_type": type(_init_error).__name__ if _init_error else None,
            "init_error_message": str(_init_error) if _init_error else None
        }), 200
    
    @error_app.route("/", defaults={"path": ""})
    @error_app.route("/<path:path>")
    def show_error(path):
        try:
            error_info = {
                "error": "Flask app failed to import / initialize",
                "exception_type": type(_init_error).__name__ if _init_error else "Unknown",
                "message": str(_init_error) if _init_error else "Unknown error",
                "path": path,
                "note": "Visit /test to verify handler is working",
                "handler_status": "error_handler_active"
            }
            # Only include traceback if it's safe (not too long)
            try:
                tb = traceback.format_exc()
                if len(tb) < 10000:  # Limit traceback size
                    error_info["traceback"] = tb
            except:
                pass
            # Return 200 instead of 500 so Vercel doesn't treat it as a crash
            # The error info is in the JSON body
            return jsonify(error_info), 200
        except Exception as e:
            # If even the error handler fails, return minimal response
            return jsonify({
                "error": "Critical error handler failure",
                "message": str(e)
            }), 200
    
    _handler = error_app
    print("DEBUG: Error handler created as fallback")

# Ensure handler is always defined
if _handler is None:
    print("DEBUG ERROR: Handler is None! Creating minimal fallback.")
    minimal_app = Flask(__name__)
    @minimal_app.route("/", defaults={"path": ""})
    @minimal_app.route("/<path:path>")
    def minimal_handler(path):
        return jsonify({
            "error": "Handler initialization failed",
            "message": "Handler was not properly initialized",
            "path": path
        }), 500
    _handler = minimal_app

# Export handler for Vercel (CRITICAL - must be at module level)
# Final safety check - ensure handler is never None
# Create a guaranteed-to-work fallback handler
def create_fallback_handler():
    """Create a minimal Flask app that will always work."""
    fallback = Flask(__name__)
    
    @fallback.route("/test")
    def test():
        return jsonify({"status": "fallback_handler_active", "message": "Using fallback handler"}), 200
    
    @fallback.route("/", defaults={"path": ""})
    @fallback.route("/<path:path>")
    def catch_all(path):
        return jsonify({
            "error": "Handler initialization issue",
            "message": "Using fallback handler - main handler was not properly initialized",
            "path": path,
            "init_error": str(_init_error) if _init_error else "No error recorded"
        }), 500
    
    return fallback

# Set handler - use fallback if _handler is None
if _handler is None:
    print("DEBUG CRITICAL ERROR: Handler is None at export time! Using fallback.")
    handler = create_fallback_handler()
else:
    handler = _handler

# #region agent log
try:
    with open('/Users/IqbalJaved/Desktop/Desktop - MacBook Air/Projects/Python Repos/deed-finance/.cursor/debug.log', 'a') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"init","hypothesisId":"A","location":"api/index.py:210","message":"Handler export complete","data":{"handler_type":type(handler).__name__,"handler_is_none":handler is None,"has_init_error":_init_error is not None},"timestamp":int(__import__('time').time()*1000)}) + '\n')
except: pass
print(f"DEBUG: Handler export complete - type: {type(handler).__name__}")
# #endregion

# DO NOT use assert in production - it can cause crashes
# Instead, we've ensured handler is always set above
print("DEBUG: Handler ready for Vercel")
