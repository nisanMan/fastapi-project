#auth/hashing.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# def verify_password(plain, hashed):
#     return pwd_context.verify(plain, hashed)

# def create_token(data: dict):
#     expire = datetime.utcnow() + timedelta(minutes=30)
#     data.update({"exp": expire})
#     return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)