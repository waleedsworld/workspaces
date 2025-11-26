"""Workspaces API — a small, friendly Flask REST API for managing users.

A compact CRUD service with an in-memory store, sensible validation, and
consistent JSON error handling. Great as a learning reference or a starting
point for a real backend.
"""

import os
import re

from flask import Flask, jsonify, request

app = Flask(__name__)

# A very small, deliberately loose email sanity check. It is not meant to be
# RFC-perfect — just enough to catch obvious typos like "not-an-email".
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# In-memory data store. Swap this out for a real database when you outgrow it.
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
]


def find_user(user_id):
    """Return the user dict with the given id, or None."""
    return next((u for u in users if u["id"] == user_id), None)


def email_taken(email, ignore_id=None):
    """True if another user already uses this email (case-insensitive)."""
    email = email.strip().lower()
    return any(
        u["email"].lower() == email and u["id"] != ignore_id for u in users
    )


@app.route("/")
def home():
    """Friendly index that lists the available endpoints."""
    return jsonify(
        {
            "message": "Welcome to the Workspaces API",
            "endpoints": {
                "health": "GET /health",
                "list_users": "GET /users",
                "get_user": "GET /users/<id>",
                "create_user": "POST /users",
                "update_user": "PUT /users/<id>",
                "delete_user": "DELETE /users/<id>",
            },
        }
    )


@app.route("/health")
def health():
    return jsonify({"status": "healthy", "user_count": len(users)}), 200


@app.route("/users", methods=["GET"])
def get_users():
    return jsonify({"users": users, "count": len(users)}), 200


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = find_user(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json(silent=True)

    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Name and email are required"}), 400

    name = str(data["name"]).strip()
    email = str(data["email"]).strip()

    if not name:
        return jsonify({"error": "Name cannot be empty"}), 400
    if not EMAIL_RE.match(email):
        return jsonify({"error": "A valid email is required"}), 400
    if email_taken(email):
        return jsonify({"error": "Email is already in use"}), 409

    new_id = max((u["id"] for u in users), default=0) + 1
    new_user = {"id": new_id, "name": name, "email": email}
    users.append(new_user)
    return jsonify(new_user), 201


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = find_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No update fields provided"}), 400

    if "name" in data:
        name = str(data["name"]).strip()
        if not name:
            return jsonify({"error": "Name cannot be empty"}), 400
        user["name"] = name

    if "email" in data:
        email = str(data["email"]).strip()
        if not EMAIL_RE.match(email):
            return jsonify({"error": "A valid email is required"}), 400
        if email_taken(email, ignore_id=user_id):
            return jsonify({"error": "Email is already in use"}), 409
        user["email"] = email

    return jsonify(user), 200


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    global users
    user = find_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    users = [u for u in users if u["id"] != user_id]
    return jsonify({"message": "User deleted successfully"}), 200


@app.errorhandler(404)
def not_found(_error):
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(405)
def method_not_allowed(_error):
    return jsonify({"error": "Method not allowed for this endpoint"}), 405


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "5000"))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() in ("1", "true", "yes")
    app.run(debug=debug, host=host, port=port)
