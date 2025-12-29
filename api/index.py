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
import json

# #region agent log
try:
    with open('/Users/IqbalJaved/Desktop/Desktop - MacBook Air/Projects/Python Repos/deed-finance/.cursor/debug.log', 'a') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"typing-extensions-test","hypothesisId":"A","location":"api/index.py:15","message":"Handler init started","data":{"python_version":sys.version,"sys_path_len":len(sys.path)},"timestamp":int(__import__('time').time()*1000)}) + '\n')
except: pass
# #endregion

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# #region agent log
try:
    import typing_extensions
    te_version = getattr(typing_extensions, '__version__', 'unknown')
    te_path = getattr(typing_extensions, '__file__', 'unknown')
    with open('/Users/IqbalJaved/Desktop/Desktop - MacBook Air/Projects/Python Repos/deed-finance/.cursor/debug.log', 'a') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"typing-extensions-test","hypothesisId":"A","location":"api/index.py:25","message":"typing-extensions check","data":{"version":te_version,"path":te_path,"is_vendor":'_vendor' in str(te_path)},"timestamp":int(__import__('time').time()*1000)}) + '\n')
except Exception as e:
    try:
        with open('/Users/IqbalJaved/Desktop/Desktop - MacBook Air/Projects/Python Repos/deed-finance/.cursor/debug.log', 'a') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"typing-extensions-test","hypothesisId":"A","location":"api/index.py:30","message":"typing-extensions import failed","data":{"error":str(e)},"timestamp":int(__import__('time').time()*1000)}) + '\n')
    except: pass
# #endregion

# Import Flask for error handler
from flask import Flask, jsonify

# Initialize handler variable
_handler = None

# #region agent log
try:
    with open('/Users/IqbalJaved/Desktop/Desktop - MacBook Air/Projects/Python Repos/deed-finance/.cursor/debug.log', 'a') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"typing-extensions-test","hypothesisId":"B","location":"api/index.py:40","message":"About to import app","data":{},"timestamp":int(__import__('time').time()*1000)}) + '\n')
except: pass
# #endregion

# Try to import the app - use simple import
# The issue is Vercel's runtime scanning, not our import method
try:
    from app import app
    _handler = app
    # #region agent log
    try:
        with open('/Users/IqbalJaved/Desktop/Desktop - MacBook Air/Projects/Python Repos/deed-finance/.cursor/debug.log', 'a') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"typing-extensions-test","hypothesisId":"B","location":"api/index.py:48","message":"App imported successfully","data":{},"timestamp":int(__import__('time').time()*1000)}) + '\n')
    except: pass
    # #endregion
    print("DEBUG: App imported successfully")
except Exception as e:
    # #region agent log
    try:
        import traceback as tb
        tb_str = ''.join(tb.format_exception(type(e), e, e.__traceback__))
        with open('/Users/IqbalJaved/Desktop/Desktop - MacBook Air/Projects/Python Repos/deed-finance/.cursor/debug.log', 'a') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"typing-extensions-test","hypothesisId":"B","location":"api/index.py:55","message":"App import failed","data":{"error_type":type(e).__name__,"error_msg":str(e),"traceback":tb_str[:500]},"timestamp":int(__import__('time').time()*1000)}) + '\n')
    except: pass
    # #endregion
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

# #region agent log
# Log what's in the module namespace before cleanup
try:
    module_attrs = [k for k in globals().keys() if not k.startswith('_') and k != 'handler']
    with open('/Users/IqbalJaved/Desktop/Desktop - MacBook Air/Projects/Python Repos/deed-finance/.cursor/debug.log', 'a') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"vercel-scan-test","hypothesisId":"E","location":"api/index.py:170","message":"Module namespace before cleanup","data":{"attrs":module_attrs[:20],"handler_type":str(type(_handler))},"timestamp":int(__import__('time').time()*1000)}) + '\n')
except: pass
# #endregion

# Clean up ALL temporary variables and imports
# Vercel's runtime scans module attributes - we need to ensure ONLY 'handler' is visible
# The error suggests Vercel is finding 'Base' (from SQLAlchemy) and trying issubclass() on it
_vars_to_delete = ['_handler', 'parent_dir', 'error_app', 'fallback', 'error_handler', 
                   'json', 'sys', 'os', 'Flask', 'jsonify', 'typing_extensions', 'te_version', 'te_path']
for var in _vars_to_delete:
    try:
        if var in globals():
            del globals()[var]
    except (NameError, KeyError):
        pass
del _vars_to_delete

# #region agent log
# Log what's left after cleanup
try:
    final_attrs = [k for k in globals().keys() if not k.startswith('_')]
    with open('/Users/IqbalJaved/Desktop/Desktop - MacBook Air/Projects/Python Repos/deed-finance/.cursor/debug.log', 'a') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"vercel-scan-test","hypothesisId":"E","location":"api/index.py:190","message":"Module namespace after cleanup","data":{"attrs":final_attrs[:20],"has_handler":"handler" in globals()},"timestamp":int(__import__('time').time()*1000)}) + '\n')
except: pass
# #endregion

print("DEBUG: Handler exported and ready")
