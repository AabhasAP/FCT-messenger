from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List, Optional
from app.db.postgresql import get_db
from app.models.user import User, UserPresence, PresenceStatus
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    avatar_url: Optional[str]
    is_active: bool
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None

class PresenceUpdate(BaseModel):
    status: PresenceStatus
    custom_status: Optional[str] = None

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user profile."""
    return current_user

@router.patch("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update current user profile."""
    if user_update.full_name:
        current_user.full_name = user_update.full_name
    if user_update.avatar_url:
        current_user.avatar_url = user_update.avatar_url
    
    await db.commit()
    await db.refresh(current_user)
    return current_user

@router.post("/presence")
async def update_presence(
    presence_update: PresenceUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update user presence status."""
    result = await db.execute(select(UserPresence).where(UserPresence.user_id == current_user.id))
    presence = result.scalar_one_or_none()
    
    if presence:
        presence.status = presence_update.status
        presence.custom_status = presence_update.custom_status
    else:
        presence = UserPresence(
            user_id=current_user.id,
            status=presence_update.status,
            custom_status=presence_update.custom_status
        )
        db.add(presence)
    
    await db.commit()
    return {"status": "updated"}

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get user by ID."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
