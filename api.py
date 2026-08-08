import sys
import os

# Allow importing app.py and chatbot.py from the project root
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app import app

# Vercel's Python runtime looks for a variable named `app` (WSGI callable)