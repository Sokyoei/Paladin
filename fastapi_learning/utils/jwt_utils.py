from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError
from loguru import logger

from fastapi_learning.config import settings


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """生成JWT令牌

    Args:
        data(dict): 令牌信息
        expires_delta(timedelta | None): 过期时间，默认为 JWT_ACCESS_TOKEN_EXPIRE_MINUTES

    Returns:
        str: 令牌字符串
    """
    to_encode = data.copy()
    now = datetime.now(UTC)
    # 设置过期时间（UTC时间，避免时区问题）
    expire = now + expires_delta if expires_delta else now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "iat": now})
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])

    encoded_jwt = jwt.encode(claims=to_encode, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str) -> dict:
    """验证 JWT 令牌

    Args:
        token(str): JWT 令牌

    Returns:
        dict: 验证成功返回令牌载荷

    Raises:
        ExpiredSignatureError: 令牌已过期
        JWTError: 令牌签名错误/被篡改/非法，或缺少必要的 exp 声明
    """
    try:
        return jwt.decode(
            token=token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_exp": True, "require": ["exp"]},
        )
    except (ExpiredSignatureError, JWTError):
        logger.error("令牌验证失败")
        raise
