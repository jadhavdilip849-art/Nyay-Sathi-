"""
Root launcher for Nyaya Sathi Web Application.
Usage:
  python run.py
  python run.py --port 8080 --host 0.0.0.0
"""

import sys
import os
import argparse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Ensure app package is in path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.server import run_server
from app.config import HOST, PORT

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nyaya Sathi Web Server")
    parser.add_argument("--host", default=HOST, help="Host address to bind to (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=PORT, help="Port to listen on (default: 8080)")
    args = parser.parse_args()

    run_server(host=args.host, port=args.port)
