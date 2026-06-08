from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from schemas.user import UserRequest
from crud import user

router = APIRouter(prefix="/api/user", tags=["user"])

@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    #注册逻辑：验证用户是否存在 -> 创建用户 -> 生成token令牌 -> 响应结果
    existing_user = await user.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")

    user1 = await user.create_user(db, user_data)

    return {
        "message": "success",
        "data": {
            "username": user1.username,
            "nickname": user1.nickname,
        }
    }