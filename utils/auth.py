from email.policy import HTTP
from http.client import HTTPException

from fastapi import Header
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_config import get_db
from crud import user

# 整合 根据Token 查询用户，返回用户
async def get_current_user(
        authorization: str = Header(..., alias="Authorization"),
        db = Depends(get_db)
):
    token = authorization.replace("Bearer ", "")
    existing_user = await user.get_user_by_token(db, token)

    if not existing_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的令牌或已经过期的令牌")

    return existing_user