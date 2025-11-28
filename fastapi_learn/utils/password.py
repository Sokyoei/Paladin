from passlib.context import CryptContext

# password hash settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str | bytes, hashed_password: str | bytes) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def password_hash(password: str | bytes) -> str:
    return pwd_context.hash(password)
