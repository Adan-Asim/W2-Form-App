import os

from dotenv import load_dotenv

load_dotenv()


FLASK_ENV = "production"
DEBUG = False

SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DB_URI", "postgresql://Adan:password1!@localhost/w2form"
)
FLASK_LOGIN_SECRET_KEY = os.environ.get(
    "FLASK_LOGIN_SECRET_KEY", "flask_login_secret_key"
)

FORM_DATA_ENCRYPTION_KEY = os.environ.get(
    "FORM_DATA_ENCRYPTION_KEY"
)

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

ENABLE_OPENAI_SERVICES = os.getenv("ENABLE_OPENAI_SERVICES", "False") == "True"

