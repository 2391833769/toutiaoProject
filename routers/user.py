from select import select

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_config import get_db
from models.user import User
from schemas.user import UserRequest, UserInfoBase, UserAuthResponse, UserInfoResponse, UserUpdateRequest, \
    UserChangePasswordRequest
from crud import user
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/user", tags=["user"])

@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    #注册逻辑：验证用户是否存在 -> 创建用户 -> 生成token令牌 -> 响应结果
    existing_user = await user.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")

    user1 = await user.create_user(db, user_data)
    token = await user.create_token(db, user1.id)
    print(UserInfoResponse.model_validate(user1))
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user1))
    return success_response(message="注册成功", data=response_data)



@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 登录逻辑: 验证用户是否存在 -> 验证密码 -> 生成Token -> 响应结果
    existing_user = await user.authenticate_user(db, user_data.username, user_data.password)
    token = await user.create_token(db, existing_user.id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")

    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(existing_user))
    return success_response(message="登录成功啦", data=response_data)



@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
    return success_response(message="获取用户信息成功", data=UserInfoResponse.model_validate(user))



@router.put("/update")
async def update_user_info(
        user_data: UserUpdateRequest,
        existing_user: User =  Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    print(existing_user, 'existing')
    users = await user.update_user(db, existing_user.username, user_data)
    return success_response(message="更新用户信息成功", data=UserInfoResponse.model_validate(users))


@router.put("/password")
async def update_password(
        password_data: UserChangePasswordRequest,
        existing_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    res_change_pwd = await user.change_password(db, existing_user, password_data.old_password, password_data.new_password)
    if not res_change_pwd:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="旧密码错误")

    return success_response(message="修改密码成功", data=UserInfoResponse.model_validate(existing_user))

