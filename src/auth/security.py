from passlib.hash import pbkdf2_sha256
import jwt
from datetime import datetime, timedelta
from src.config import SECRET_KEY


def generate_token(obj):
    payload = {
        "id": str(obj.id),
        "name": obj.name,
        "username": obj.username,
        "is_admin": obj.is_admin,
        "exp": datetime.utcnow() + timedelta(minutes=120),
    }
    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm="HS256")
    return token


def encode_password(password):
    hashed_password = pbkdf2_sha256.hash(password)
    return hashed_password


def decode_password(password, hashed_password):
    response = pbkdf2_sha256.verify(password, hashed_password)
    return response
