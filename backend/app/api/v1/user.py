"""
一点灵光 - 用户信息API模块
处理用户信息的查询和更新
"""
from fastapi import APIRouter, HTTPException
from app.schemas.task import UserInfoResponse, UserUpdateRequest
from app.core.task_manager import task_manager

router = APIRouter()

# 默认用户ID（演示用）
DEFAULT_USER_ID = "default-user-001"


@router.get("/info", response_model=UserInfoResponse)
async def get_user_info():
    """
    获取当前用户信息
    
    Returns:
        UserInfoResponse: 用户信息
    """
    user = task_manager.get_user(DEFAULT_USER_ID)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserInfoResponse(
        code=0,
        data=user.to_dict()
    )


@router.put("/info", response_model=UserInfoResponse)
async def update_user_info(request: UserUpdateRequest):
    """
    更新当前用户信息
    
    Args:
        request: 包含要更新的字段
    
    Returns:
        UserInfoResponse: 更新后的用户信息
    """
    update_data = request.model_dump(exclude_none=True)
    success = task_manager.update_user(DEFAULT_USER_ID, **update_data)
    
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = task_manager.get_user(DEFAULT_USER_ID)
    return UserInfoResponse(
        code=0,
        data=user.to_dict()
    )
