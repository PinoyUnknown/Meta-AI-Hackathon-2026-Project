"""
MetaHorizon Odyssey 3D - Dedicated 3D Game Launcher
Launches the 3D WebGL hardware-accelerated game with procedural audio synthesizer,
glitch post-processing shaders, and 5 progressive stages.
"""

import os
import sys
import webbrowser
import threading
import http.server
import socketserver

GAME_3D_DIR = os.path.dirname(os.path.abspath(__file__))

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=GAME_3D_DIR, **kwargs)
    def log_message(self, format, *args):
        pass  # Suppress HTTP request logs for clean console

def start_local_game_server(port: int = 8088):
    """Starts a lightweight daemon HTTP server for 3D game assets."""
    socketserver.TCPServer.allow_reuse_address = True
    try:
        httpd = socketserver.TCPServer(("127.0.0.1", port), QuietHandler)
    except OSError:
        # Fallback to alternative port
        port = 8090
        httpd = socketserver.TCPServer(("127.0.0.1", port), QuietHandler)
        
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return port

def launch_3d_game(port: int = 8088, use_window: bool = True):
    """
    Launches the 3D Game Window.
    Uses native pywebview on Windows 10 if available, with browser fallback.
    """
    server_port = start_local_game_server(port)
    game_url = f"http://127.0.0.1:{server_port}/index.html"
    print("=" * 80)
    print("  FOUNDATION: ORGANIC SETTLEMENT SIMULATOR (VIBRANT DAYTIME EDITION)")
    print(f"  Game Engine Server Active: {game_url}")
    print("  Controls: WASD (Pan View) | Right-Drag (Rotate) | Mouse Scroll (Zoom 8m-260m)")
    print("            Click (Build / Inspect) | R (Rotate Structure) | ESC (Settings)")
    print("=" * 80)

    if use_window:
        try:
            import webview
            print("[ENGINE] Launching Hardware-Accelerated Daytime 3D Window (WebView2)...")
            window = webview.create_window(
                title="FOUNDATION: ORGANIC SETTLEMENT SIMULATOR",
                url=game_url,
                width=1280,
                height=760,
                resizable=True,
                background_color="#7ec0ee"
            )
            webview.start()
            return
        except Exception as e:
            print(f"[ENGINE] Native window fallback ({str(e)}). Opening in browser:")

    # Fallback to default browser
    webbrowser.open(game_url)
    print("[3D ENGINE] 3D Game launched in browser. Press Ctrl+C in terminal to stop.")
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[3D ENGINE] Shutdown complete.")

if __name__ == "__main__":
    launch_3d_game()
