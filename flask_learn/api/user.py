import asyncio

from flask import Blueprint

bp = Blueprint('user', __name__)


@bp.route("/user")
async def create_user():
    await asyncio.sleep(1)
    return "user"
