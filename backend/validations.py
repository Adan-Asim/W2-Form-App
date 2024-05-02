from datetime import datetime
from flask import jsonify
import re


def validate_signup_params(email, name, password):
    if not email or not name or not password:
        return jsonify(message="All fields are required"), 400

    if len(password) < 6:
        return jsonify(message="Password must be at least 6 characters long"), 400
    if len(name) < 3:
        return jsonify(message="Name must be at least xx2 characters long"), 400
    if not is_valid_email(email):
        return jsonify(message="Invalid email"), 400

    return None


def validate_login_params(email, password):
    if not email or not password:
        return (
            jsonify(message="Please provide email and password"),
            400,
        )
    if len(password) < 6:
        return jsonify(message="Password must be at least 6 characters long"), 400

    return None


def is_valid_email(email):
    pattern = re.compile(r"^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$")
    return bool(re.match(pattern, email))


def validate_file_upload(file):
    if not file:
        return jsonify(message="No file provided"), 400

    if file.filename == "":
        return jsonify(message="No selected file"), 400

    if (
        file.filename.endswith(".mp4")
        or file.filename.endswith(".avi")
        or file.filename.endswith(".mov")
        or file.filename.endswith(".wmv")
        or file.filename.endswith(".flv")
    ):
        return (
            jsonify(message="Invalid file format: videos are not allowed"),
            400,
        )

    return None


def validate_user_query_params(query, file_id):
    if not query or not file_id:
        return jsonify(message="User query and file selection is required"), 400
