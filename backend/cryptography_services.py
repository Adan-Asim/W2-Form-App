from cryptography.fernet import Fernet
from config import FORM_DATA_ENCRYPTION_KEY

cipher_suite = Fernet(FORM_DATA_ENCRYPTION_KEY)


def encrypt_text(text):
    encrypted_text = cipher_suite.encrypt(text.encode())
    return encrypted_text


def decrypt_text(encrypted_text):
    decrypted_text = cipher_suite.decrypt(encrypted_text).decode()
    return decrypted_text
