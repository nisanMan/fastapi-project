#auth/jwt_handler.py
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "SECRET123" #"supersecret"
ALGORITHM = "HS256"


def create_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(hours=2)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

#pip install python-jose