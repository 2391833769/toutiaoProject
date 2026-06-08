from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.user import UserRequest
from utils import security


# 根据用户名查询用户
async def get_user_by_username(db: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# 创建用户
async def create_user(db: AsyncSession, user_data: UserRequest):
    # 先密码加密处理 -> add
    hashed_password = security.get_hash_password(user_data.password)
    user = User(username=user_data.username, password=hashed_password)
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user
