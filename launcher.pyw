# launcher.pyw
"""
SecureLearn Phishing Detection Simulator - GUI Controller
Runs completely without terminal using pythonw.exe
"""

import os
import sys
import time
import subprocess
import threading
import webbrowser
import urllib.request
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

# Resolve project paths
PROJECT_DIR = Path(__file__).resolve().parent
ROOT_DIR = PROJECT_DIR.parent

# Find Python / PythonW executable in venv
VENV_PYTHONW = None
possible_pyw = [
    ROOT_DIR / "venv" / "Scripts" / "pythonw.exe",
    PROJECT_DIR / "venv" / "Scripts" / "pythonw.exe",
    Path(sys.executable).parent / "pythonw.exe",
    Path(sys.executable)
]

for p in possible_pyw:
    if p.exists():
        VENV_PYTHONW = p
        break

if not VENV_PYTHONW:
    VENV_PYTHONW = Path(sys.executable)

SERVER_SCRIPT = PROJECT_DIR / "run_server.py"
PID_FILE = PROJECT_DIR / ".server.pid"
APP_URL = "http://127.0.0.1:5000"

server_process = None

def is_server_running():
    """Check if Flask server is responsive on port 5000"""
    try:
        req = urllib.request.Request(f"{APP_URL}/health", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=1.5) as response:
            return response.status == 200
    except Exception:
        return False

def start_server_process():
    """Start background server with pythonw (no terminal)"""
    global server_process
    if is_server_running():
        return True

    # Kill any stale PID if needed
    stop_server_process(silent=True)

    creationflags = 0
    if sys.platform == "win32":
        creationflags = subprocess.CREATE_NO_WINDOW | 0x08000000

    server_process = subprocess.Popen(
        [str(VENV_PYTHONW), str(SERVER_SCRIPT)],
        cwd=str(PROJECT_DIR),
        creationflags=creationflags,
        close_fds=True
    )

    # Wait up to 10 seconds for server to come online
    for _ in range(20):
        time.sleep(0.5)
        if is_server_running():
            return True
    return is_server_running()

def stop_server_process(silent=False):
    """Stop the background server"""
    global server_process
    
    # 1. Try graceful HTTP shutdown
    try:
        req = urllib.request.Request(f"{APP_URL}/api/shutdown", headers={'User-Agent': 'Mozilla/5.0'})
        urllib.request.urlopen(req, timeout=1.0)
        time.sleep(0.5)
    except Exception:
        pass

    # 2. Try PID file
    if PID_FILE.exists():
        try:
            pid = int(PID_FILE.read_text().strip())
            if sys.platform == "win32":
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], 
                               capture_output=True, creationflags=0x08000000)
            else:
                os.kill(pid, 9)
            PID_FILE.unlink(missing_ok=True)
        except Exception:
            pass

    # 3. Terminate subprocess handle if present
    if server_process and server_process.poll() is None:
        try:
            server_process.terminate()
            server_process.wait(timeout=2)
        except Exception:
            pass
        server_process = None

    if not silent:
        time.sleep(0.5)

def open_in_browser():
    """Open app in default browser"""
    webbrowser.open(APP_URL)

def open_in_app_mode():
    """Open as a standalone desktop window using Edge/Chrome App Mode"""
    # Check Edge
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    for path in edge_paths:
        if os.path.exists(path):
            subprocess.Popen([path, f"--app={APP_URL}", "--window-size=1200,800"])
            return

    # Check Chrome
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]
    for path in chrome_paths:
        if os.path.exists(path):
            subprocess.Popen([path, f"--app={APP_URL}", "--window-size=1200,800"])
            return

    # Fallback to default browser
    webbrowser.open(APP_URL)

def create_desktop_shortcut():
    """Create a Windows Desktop Shortcut for 1-click launch"""
    try:
        desktop = Path(os.environ.get("USERPROFILE", "")) / "Desktop"
        if not desktop.exists():
            desktop = Path(os.path.expanduser("~/Desktop"))
        
        shortcut_vbs = PROJECT_DIR / "Start_App.vbs"
        shortcut_path = desktop / "SecureLearn Phishing Simulator.lnk"

        vbs_script = f'''
        Set oWS = WScript.CreateObject("WScript.Shell")
        sLinkFile = "{shortcut_path}"
        Set oLink = oWS.CreateShortcut(sLinkFile)
        oLink.TargetPath = "wscript.exe"
        oLink.Arguments = """{shortcut_vbs}"""
        oLink.WorkingDirectory = "{PROJECT_DIR}"
        oLink.Description = "Launch SecureLearn Phishing Detection Simulator"
        oLink.Save
        '''
        
        temp_vbs = PROJECT_DIR / "_mklink.vbs"
        temp_vbs.write_text(vbs_script, encoding='utf-8')
        subprocess.run(["cscript", "//Nologo", str(temp_vbs)], capture_output=True)
        temp_vbs.unlink(missing_ok=True)
        
        messagebox.showinfo("Success", "Desktop shortcut created successfully!\n\nYou can now launch the app directly from your Desktop with 1-click.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not create shortcut: {e}")


# ==================== GUI APPLICATION ====================

class AppLauncherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SecureLearn Phishing Lab - Controller")
        self.root.geometry("480x420")
        self.root.resizable(False, False)
        
        # Windows styling
        self.root.configure(bg="#0f172a")

        # Header Frame
        header = tk.Frame(root, bg="#1e293b", pady=15)
        header.pack(fill="x")

        title_lbl = tk.Label(
            header,
            text="🛡️ SecureLearn Cyber Lab",
            font=("Segoe UI", 16, "bold"),
            fg="#38bdf8",
            bg="#1e293b"
        )
        title_lbl.pack()

        subtitle_lbl = tk.Label(
            header,
            text="AI-Powered Phishing Detection & Awareness Platform",
            font=("Segoe UI", 9),
            fg="#94a3b8",
            bg="#1e293b"
        )
        subtitle_lbl.pack(pady=(2, 0))

        # Status Card
        status_card = tk.Frame(root, bg="#1e293b", bd=1, relief="solid", pady=12, padx=15)
        status_card.pack(fill="x", padx=25, pady=15)

        self.status_indicator = tk.Label(
            status_card,
            text="●",
            font=("Segoe UI", 16),
            fg="#ef4444",
            bg="#1e293b"
        )
        self.status_indicator.pack(side="left", padx=(5, 10))

        self.status_text = tk.Label(
            status_card,
            text="Server: Stopped",
            font=("Segoe UI", 11, "bold"),
            fg="#f8fafc",
            bg="#1e293b",
            anchor="w"
        )
        self.status_text.pack(side="left", fill="x")

        # Action Buttons Container
        btn_frame = tk.Frame(root, bg="#0f172a")
        btn_frame.pack(fill="both", expand=True, padx=25, pady=5)

        # Start & Open Button (Primary)
        self.btn_start = tk.Button(
            btn_frame,
            text="🚀  Start Server & Open App",
            font=("Segoe UI", 11, "bold"),
            bg="#0284c7",
            fg="white",
            activebackground="#0369a1",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            pady=10,
            command=self.on_start_clicked
        )
        self.btn_start.pack(fill="x", pady=4)

        # Open in Standalone Window Mode
        self.btn_app_mode = tk.Button(
            btn_frame,
            text="🖥️  Open in Desktop App Window",
            font=("Segoe UI", 10),
            bg="#334155",
            fg="#f8fafc",
            activebackground="#475569",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            pady=6,
            command=self.on_app_mode_clicked
        )
        self.btn_app_mode.pack(fill="x", pady=4)

        # Stop Server Button
        self.btn_stop = tk.Button(
            btn_frame,
            text="🛑  Stop Server",
            font=("Segoe UI", 10),
            bg="#334155",
            fg="#f87171",
            activebackground="#475569",
            activeforeground="#f87171",
            relief="flat",
            cursor="hand2",
            pady=6,
            command=self.on_stop_clicked
        )
        self.btn_stop.pack(fill="x", pady=4)

        # Create Desktop Shortcut
        self.btn_shortcut = tk.Button(
            btn_frame,
            text="📌  Create Desktop Shortcut",
            font=("Segoe UI", 9),
            bg="#1e293b",
            fg="#94a3b8",
            activebackground="#334155",
            activeforeground="#f8fafc",
            relief="flat",
            cursor="hand2",
            pady=4,
            command=create_desktop_shortcut
        )
        self.btn_shortcut.pack(fill="x", pady=(8, 4))

        # Footer
        footer_lbl = tk.Label(
            root,
            text="Runs 100% offline & without terminal • http://127.0.0.1:5000",
            font=("Segoe UI", 8),
            fg="#64748b",
            bg="#0f172a"
        )
        footer_lbl.pack(side="bottom", pady=8)

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Start periodic status checker thread
        self.running_loop = True
        self.status_thread = threading.Thread(target=self.status_monitor, daemon=True)
        self.status_thread.start()

    def update_ui_status(self, running):
        if running:
            self.status_indicator.config(fg="#22c55e", text="●")
            self.status_text.config(text="Server: Running (http://127.0.0.1:5000)", fg="#22c55e")
            self.btn_start.config(text="🌐  Open in Browser", bg="#16a34a", activebackground="#15803d")
            self.btn_stop.config(state="normal", bg="#ef4444", fg="white", activebackground="#dc2626")
            self.btn_app_mode.config(state="normal")
        else:
            self.status_indicator.config(fg="#ef4444", text="●")
            self.status_text.config(text="Server: Stopped", fg="#94a3b8")
            self.btn_start.config(text="🚀  Start Server & Open App", bg="#0284c7", activebackground="#0369a1")
            self.btn_stop.config(state="disabled", bg="#1e293b", fg="#64748b")
            self.btn_app_mode.config(state="disabled")

    def status_monitor(self):
        while self.running_loop:
            running = is_server_running()
            try:
                self.root.after(0, self.update_ui_status, running)
            except Exception:
                pass
            time.sleep(2)

    def on_start_clicked(self):
        def task():
            if not is_server_running():
                self.btn_start.config(text="⏳  Starting server...", state="disabled")
                started = start_server_process()
                if started:
                    open_in_browser()
                else:
                    messagebox.showerror("Error", "Could not start server. Please check requirements.")
            else:
                open_in_browser()
            self.btn_start.config(state="normal")

        threading.Thread(target=task, daemon=True).start()

    def on_app_mode_clicked(self):
        if is_server_running():
            open_in_app_mode()
        else:
            def task():
                self.btn_app_mode.config(state="disabled")
                if start_server_process():
                    open_in_app_mode()
                self.btn_app_mode.config(state="normal")
            threading.Thread(target=task, daemon=True).start()

    def on_stop_clicked(self):
        def task():
            self.btn_stop.config(text="⏳  Stopping...", state="disabled")
            stop_server_process()
            self.btn_stop.config(text="🛑  Stop Server", state="normal")
        threading.Thread(target=task, daemon=True).start()

    def on_closing(self):
        self.running_loop = False
        # If server is running, ask or just minimize/close
        self.root.destroy()


def main():
    root = tk.Tk()
    app = AppLauncherGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
