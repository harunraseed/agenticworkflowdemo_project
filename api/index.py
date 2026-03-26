"""
Vercel serverless entry point.

This file wraps the Flask app so Vercel can serve it as a serverless function.
All routes (/, /api/projects, etc.) are handled by the Flask app.
"""

import sys
import os

# Add the app directory to the Python path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from app import app

# Vercel looks for an `app` variable (WSGI-compatible) in this file.
# Flask's app object is already WSGI-compatible, so this just works.
