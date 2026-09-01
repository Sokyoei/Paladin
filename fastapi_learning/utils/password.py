from pwdlib import PasswordHash

# password hash settings
ph = PasswordHash.recommended()


def verify_password(plain_password: str | bytes, hashed_password: str | bytes) -> bool:
    return ph.verify(plain_password, hashed_password)


def password_hash(password: str | bytes) -> str:
    return ph.hash(password)
