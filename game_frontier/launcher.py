"""Frontier prototype launcher: serves game_frontier/ and opens the game.

Usage:
  python launcher.py            # serve on 127.0.0.1:8089 and open in browser
  python launcher.py --port 8091
  python launcher.py --no-open  # serve only (for headless checks)
"""
import http.server
import socketserver
import sys
import threading
import webbrowser
from functools import partial

GAME_DIR = __file__.rsplit('\\', 1)[0].rsplit('/', 1)[0] if '\\' in __file__ or '/' in __file__ else '.'


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=GAME_DIR, **kwargs)

    def log_message(self, *args):
        pass


def main() -> None:
    port = 8089
    do_open = True
    args = sys.argv[1:]
    if '--port' in args:
        port = int(args[args.index('--port') + 1])
    if '--no-open' in args:
        do_open = False
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(('127.0.0.1', port), QuietHandler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    url = f'http://127.0.0.1:{port}/index.html'
    print(f'FRONTIER PROTOTYPE serving: {url}')
    print('Controls: Mouse (steer) | Space/Click (fire) | H (hangar) | M (map) | Shift (warp)')
    if do_open:
        webbrowser.open(url)
    print('Press Ctrl+C to stop.')
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        print('Stopped.')


if __name__ == '__main__':
    main()
