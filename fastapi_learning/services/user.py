import uuid
from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, exceptions
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from httpx_oauth.clients.google import GoogleOAuth2
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_learning.config import get_db, settings
from fastapi_learning.crud import UserCRUD
from fastapi_learning.models import OAuthAccount, User
from fastapi_learning.schemas import UserCreate

google_oauth_client = GoogleOAuth2(settings.GOOGLE_OAUTH_CLIENT_ID, settings.GOOGLE_OAUTH_CLIENT_SECRET)


async def get_user_db(session: Annotated[AsyncSession, Depends(get_db)]):
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.JWT_SECRET_KEY
    verification_token_secret = settings.JWT_SECRET_KEY

    def __init__(self, user_db: SQLAlchemyUserDatabase[User, uuid.UUID]):
        super().__init__(user_db)
        self.session = user_db.session

    async def on_after_register(self, user: User, request: Request | None = None):
        logger.info(f"User {user.id} has registered.")

    async def on_after_forgot_password(self, user: User, token: str, request: Request | None = None):
        logger.info(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(self, user: User, token: str, request: Request | None = None):
        logger.info(f"Verification requested for user {user.id}. Verification token: {token}")

    async def create(self, user_create: UserCreate, safe: bool = False, request: Request | None = None) -> User:
        await self.validate_password(user_create.password, user_create)

        # 唯一性校验：email / phone（uid 由系统自动生成，无需校验）
        if user_create.email is not None:
            existing_user = await self.user_db.get_by_email(user_create.email)
            if existing_user is not None:
                raise exceptions.UserAlreadyExists()
        if user_create.phone is not None:
            existing_user = await UserCRUD.get_by_phone(self.session, user_create.phone)
            if existing_user is not None:
                raise exceptions.UserAlreadyExists()

        user_dict = user_create.create_update_dict() if safe else user_create.create_update_dict_superuser()
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["uid"] = await UserCRUD.generate_uid(self.session)

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user

    async def authenticate(self, credentials: OAuth2PasswordRequestForm) -> User | None:
        """支持 email / phone / uid 多种标识登录，密码正确返回 User，否则返回 None。"""
        identifier = credentials.username.strip()

        # 1) 按 email 查找
        user = await self._get_by_email(identifier)
        # 2) 按 phone 查找
        if user is None:
            user = await UserCRUD.get_by_phone(self.session, identifier)
        # 3) 按 uid（数字）查找
        if user is None:
            try:
                user = await UserCRUD.get_by_uid(self.session, int(identifier))
            except ValueError:
                user = None

        if user is None:
            # 跑一次哈希以缓解时序攻击（与基类一致）
            self.password_helper.hash(credentials.password)
            return None

        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None
        # 必要时升级密码哈希
        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})

        return user

    async def _get_by_email(self, email: str) -> User | None:
        if not email:
            return None
        return await self.user_db.get_by_email(email)


async def get_user_manager(user_db: Annotated[SQLAlchemyUserDatabase, Depends(get_user_db)]):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy[User, uuid.UUID]:
    return JWTStrategy(secret=settings.JWT_SECRET_KEY, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(name="jwt", transport=bearer_transport, get_strategy=get_jwt_strategy)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
