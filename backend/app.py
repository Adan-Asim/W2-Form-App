from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask import request
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
    unset_jwt_cookies,
)

import config
from extensions import db

import validations as validations
import services
import bcrypt_services as bcrypt

app = Flask(__name__)
app.config.from_object(config)
CORS(app, supports_credentials=True)

db.init_app(app)
migrate = Migrate(app, db)

app.config["SECRET_KEY"] = config.FLASK_LOGIN_SECRET_KEY
jwt = JWTManager(app)


@app.route("/")
def index():
    return jsonify(message="Hello from W2 Chat Form")


@app.route("/api/user/signup", methods=["POST"])
def signup():
    email = request.json.get("email")
    name = request.json.get("name")
    password = request.json.get("password")

    validation_error = validations.validate_signup_params(email, name, password)
    if validation_error:
        return validation_error

    user = services.get_existing_user(email)
    if user:
        return jsonify(message="A user already exists with these details"), 409

    email = email.lower()
    password = bcrypt.hash_password(password)

    user = services.create_user(email, name, password)

    if not user:
        return jsonify(message="User could not be created"), 403

    return jsonify(message="User created successfully"), 201


@app.route("/api/user/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    validation_error = validations.validate_login_params(email, password)
    if validation_error:
        return validation_error

    user = services.get_user_by_email(email)
    if user:
        if bcrypt.check_password(password, user.password):
            import datetime

            token_validity_duration = datetime.timedelta(days=90)

            access_token = create_access_token(
                identity=user.id, expires_delta=(token_validity_duration)
            )
            response = jsonify(
                message="User login successful", access_token=access_token
            )
            return response, 200

    response = jsonify(
        message="Unable to log in, make sure given credentials are correct"
    )
    return response, 401


@app.route("/api/user/logout")
@jwt_required()
def logout():
    res = jsonify(message="User logout successful")
    unset_jwt_cookies(res)
    return res, 200


@app.route("/api/file/upload", methods=["POST"])
@jwt_required()
def upload_w2_form():
    current_user_id = get_jwt_identity()

    file = request.files["file"]
    validation_errors = validations.validate_file_upload(request.files["file"])
    if validation_errors:
        return validation_errors

    file_id = services.handle_file_upload(file, current_user_id)
    if file_id:
        return jsonify({"message": "File uploaded and parsed successfully"}), 200

    return jsonify({"message": "File upload failed"}), 500


@app.route("/api/user/files", methods=["GET"])
@jwt_required()
def get_user_files():
    current_user_id = get_jwt_identity()
    return services.get_user_files_info(current_user_id)


@app.route("/api/ask", methods=["POST"])
@jwt_required()
def ask_question():
    user_query = request.json["query"]
    file_id = request.json["file_id"]
    current_user_id = get_jwt_identity()

    validation_errors = validations.validate_user_query_params(user_query, file_id)
    if validation_errors:
        return validation_errors

    response = services.handle_user_query(user_query, file_id, current_user_id)
    if not response:
        return jsonify({"message": "Error processing user query"}), 500

    return jsonify({"ai_response": response}), 200


@app.route("/api/user/chat-history", methods=["GET"])
@jwt_required()
def get_user_chat_history():
    current_user_id = get_jwt_identity()
    return services.get_user_chat_history(current_user_id)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
