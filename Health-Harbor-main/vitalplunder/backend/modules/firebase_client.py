"""Firebase Admin bootstrap and helpers for auth + Firestore.

Set FIREBASE_CREDENTIALS_PATH or GOOGLE_APPLICATION_CREDENTIALS to your service
account JSON. The file stays local and should not be committed.
"""

import os
from functools import wraps

import firebase_admin
from firebase_admin import auth as fb_auth
from firebase_admin import credentials, firestore
from flask import jsonify, request


_app = None
_db = None


def _get_cred_path() -> str:
    path = os.getenv("FIREBASE_CREDENTIALS_PATH") or os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not path:
        raise RuntimeError("Firebase credentials path not set. Set FIREBASE_CREDENTIALS_PATH or GOOGLE_APPLICATION_CREDENTIALS.")
    if not os.path.exists(path):
        raise RuntimeError(f"Firebase credentials file not found at: {path}")
    return path


def get_app():
    global _app
    if _app is None:
        cred = credentials.Certificate(_get_cred_path())
        _app = firebase_admin.initialize_app(cred)
    return _app


def get_db():
    global _db
    if _db is None:
        get_app()
        _db = firestore.client()
    return _db


def verify_id_token(token: str):
    get_app()
    return fb_auth.verify_id_token(token)


def require_firebase_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "missing token"}), 401
        token = auth_header.split(" ", 1)[1]
        try:
            decoded = verify_id_token(token)
        except Exception:
            return jsonify({"error": "invalid token"}), 401
        request.firebase_user = decoded
        return fn(*args, **kwargs)

    return wrapper
