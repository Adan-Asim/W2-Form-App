from model import User, W2Form, ChatHistory
from extensions import db
import logging
from flask import jsonify
import tempfile
from werkzeug.utils import secure_filename
import os
import pytesseract
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import cryptography_services
import base64
import openai_services
from collections import defaultdict
import pandas as pd
import textract


def create_user(email, name, password):
    try:
        user = User(
            email=email,
            name=name,
            password=password,
        )
        db.session.add(user)
        db.session.commit()
        return user
    except Exception as e:
        logging.error(e)
        return None


def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    return user


def get_existing_user(email):
    user = get_user_by_email(email)
    if user:
        return user

    return None


def get_user_by_id(user_id):
    user = User.query.get(int(user_id))
    return user


def handle_file_upload(file, user_id):
    try:
        _, temp_extension = os.path.splitext(file.filename)
        temp_file = tempfile.NamedTemporaryFile(suffix=temp_extension, delete=False)
        file.save(temp_file.name)

        extracted_text = extract_text_from_file(temp_file.name)
        if not extracted_text:
            return None

        extracted_full_text = "\n".join(extracted_text)
        encrypted_text = cryptography_services.encrypt_text(extracted_full_text)
        encoded_base64text = base64.b64encode(encrypted_text).decode("utf-8")

        w2_form = W2Form(
            user_id=user_id,
            filename=secure_filename(file.filename),
            data=extracted_text,
        )
        db.session.add(w2_form)
        db.session.commit()

        return w2_form.id
    except Exception as e:
        logging.error(e)
        print(e)
        return None


def extract_text_from_file(filepath):
    try:
        _, file_extension = os.path.splitext(filepath)

        if file_extension.lower() == ".pdf":
            extracted_text = extract_text_from_pdf(filepath)
        elif file_extension.lower() in [".jpg", ".jpeg", ".png"]:
            extracted_text = extract_text_from_image(filepath)
        elif file_extension.lower() in [".csv", ".xls", ".xlsx"]:
            extracted_text = extract_text_from_table(filepath)
        elif file_extension.lower() in [".txt", ".rtf", ".doc", ".docx"]:
            extracted_text = extract_text_from_text(filepath)
        else:
            raise ValueError("Unsupported file format")

        return extracted_text

    except Exception as e:
        logging.error(e)
        print(e)
        return None


def extract_text_from_pdf(filepath):
    extracted_text = []
    pages = convert_from_path(filepath)
    for page in pages:
        text = pytesseract.image_to_string(page)
        extracted_text.append(text)

    return extracted_text


def extract_text_from_image(filepath):
    with Image.open(filepath) as img:
        return pytesseract.image_to_string(img)


def extract_text_from_table(filepath):
    if filepath.lower().endswith(".csv"):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath, engine="openpyxl")
    extracted_text = "\n".join(
        df.apply(lambda row: " ".join([str(cell) for cell in row]), axis=1)
    )
    return extracted_text


def extract_text_from_text(filepath):
    return textract.process(filepath).decode("utf-8")


def get_file_by_id(file_id):
    try:
        w2_form = W2Form.query.filter_by(id=file_id).first()
        return w2_form
    except Exception as e:
        logging.error(f"Error fetching W2Form with id {file_id}: {str(e)}")
        print(f"Error fetching W2Form with id {file_id}: {str(e)}")
        return None


def get_files_by_user_id(user_id):
    w2_form = W2Form.query.filter_by(id=user_id).all()
    return w2_form


def get_user_files_info(user_id):
    user_files = get_files_by_user_id(user_id)

    if not user_files:
        return jsonify({"error": "No file found for current user"}), 400

    files = []
    for file in user_files:
        form_data = {
            "id": file.id,
            "filename": file.filename,
        }
        files.append(form_data)

    return jsonify({"files": files}), 200


def handle_user_query(user_query, file_id, current_user_id):
    try:
        extracted_data = get_file_by_id(file_id)
        extracted_data_str = "\n".join(extracted_data.data)
        extracted_data = (
            "This is extracted data from file with ID: " + extracted_data_str
        )

        show_ssn = False
        if "password" in user_query.lower():
            parts = user_query.split(":")
            if len(parts) == 2:
                _, password = parts
                password = password.strip()

                user = get_user_by_id(current_user_id)
                if user:
                    import bcrypt_services as bcrypt

                    if bcrypt.check_password(password, user.password):
                        show_ssn = True
                        user_query = "Tell me my social security number/ssn."
                    else:
                        response = "Incorrect password provided, to get ssn please enter correct password"
                        log_chat_history(current_user_id, file_id, user_query, response)
                        return response
                else:
                    response = "No user found with given ID"
                    logging.error(response)
                    log_chat_history(current_user_id, file_id, user_query, response)
                    return "No user found with given ID"

        hide_ssn_prompt = (
            "ALSO, DON'T SHARE SOCIAL SECURITY NUMBER EVER, just say you need to be authorized for getting it, ask user to send its password in this format 'password:<password>' e.g password:MyPass to get it. "
            if not show_ssn
            else ""
        )
        prompt_content = f"Given the extracted data and query, help me answer the query based on given data, make sure to not include any additional reasoning, until explicitly asked in query to to provide details or reasoning, else just give me a concise but comprehensive answer in few words or sentences. Also, don't share anything which is not relevant to the extracted data, and handle that in a humble way. {hide_ssn_prompt} \n\n{extracted_data_str}\n\nUser Query: {user_query}\nAnswer:"

        messages = [
            {
                "role": "user",
                "content": prompt_content,
            }
        ]
        completion = openai_services.request_completion(messages)

        log_chat_history(current_user_id, file_id, user_query, completion)

        return completion

    except Exception as e:
        logging.error(f"Error processing user query: {str(e)}")
        print(f"Error processing user query: {str(e)}")
        return None


def get_user_chat_history(user_id):
    files = W2Form.query.filter_by(user_id=user_id).all()

    chat_history_by_w2_form = defaultdict(list)

    for file in files:
        chat_histories = (
            ChatHistory.query.filter_by(user_id=user_id, w2_form_id=file.id)
            .order_by(ChatHistory.timestamp)
            .all()
        )

        for chat in chat_histories:
            chat_data = {
                "user_query": chat.user_query,
                "ai_response": chat.ai_response,
                "timestamp": chat.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            }
            chat_history_by_w2_form[file.id].append(chat_data)

        if not chat_histories:
            chat_history_by_w2_form[file.id] = []

    formatted_chat_history = [
        {
            "w2_form_id": file.id,
            "filename": file.filename,
            "chat_history": chat_history_by_w2_form[file.id],
        }
        for file in files
    ]

    return jsonify({"chat_history_by_w2_form": formatted_chat_history}), 200


def log_chat_history(user_id, w2_form_id, user_query, ai_response):
    chat_history = ChatHistory(
        user_id=user_id,
        w2_form_id=w2_form_id,
        user_query=user_query,
        ai_response=ai_response,
    )
    db.session.add(chat_history)
    db.session.commit()

    return chat_history
