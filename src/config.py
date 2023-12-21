from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

SECRET_KEY = os.environ.get('SECRET_KEY')

# Database connections
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_NAME = os.environ.get('DB_NAME')

DEBUG = True if os.environ.get("DEBUG") == "True" else False