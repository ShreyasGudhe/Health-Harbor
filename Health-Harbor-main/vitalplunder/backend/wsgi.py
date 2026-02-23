"""WSGI entrypoint for production servers (e.g., Render + gunicorn)."""

from app import create_app

app = create_app()
