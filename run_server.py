# run_server.py
"""
Background Server Runner for SecureLearn Phishing Detection Simulator
Runs without requiring an open terminal window.
"""

import os
import sys
import time
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_DIR = Path(__file__).resolve().parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

# Set working directory to project root
os.chdir(PROJECT_DIR)

# Handle stdout/stderr redirection for background execution
LOG_FILE = PROJECT_DIR / "server.log"
try:
    log_out = open(LOG_FILE, "a", encoding="utf-8", buffering=1)
    sys.stdout = log_out
    sys.stderr = log_out
except Exception:
    pass

from backend.app import create_app

PID_FILE = PROJECT_DIR / ".server.pid"

def save_pid():
    """Save current process PID for clean shutdown"""
    try:
        with open(PID_FILE, "w") as f:
            f.write(str(os.getpid()))
    except Exception:
        pass

def remove_pid():
    """Remove PID file on exit"""
    try:
        if PID_FILE.exists():
            PID_FILE.unlink()
    except Exception:
        pass

def main():
    save_pid()
    try:
        app = create_app('default')
        
        # Shutdown endpoint for clean shutdown
        @app.route('/api/shutdown', methods=['POST', 'GET'])
        def shutdown():
            def delayed_exit():
                time.sleep(0.5)
                os._exit(0)
            import threading
            threading.Thread(target=delayed_exit).start()
            return {'success': True, 'message': 'Server shutting down...'}, 200

        # Run on 127.0.0.1:5000
        app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)
    finally:
        remove_pid()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        import traceback
        with open(PROJECT_DIR / "server_err.log", "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)
