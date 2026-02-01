from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from app.db.postgresql import get_db
from app.models.channel import Channel, ChannelMember, DirectMessage, ChannelType, ChannelRole
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()

class ChannelCreate(BaseModel):
    workspace_id: str
    name: str
    description: Optional[str] = None
    type: ChannelType = ChannelType.PUBLIC

class ChannelResponse(BaseModel):
    id: str
    workspace_id: str
    name: str
    description: Optional[str]
    type: ChannelType
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.post("", response_model=ChannelResponse, status_code=201)
async def create_channel(
    channel_data: ChannelCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new channel."""
    channel = Channel(
        workspace_id=channel_data.workspace_id,
        name=channel_data.name,
        description=channel_data.description,
        type=channel_data.type,
        created_by=current_user.id
    )
    db.add(channel)
    await db.flush()
    
    # Add creator as admin
    member = ChannelMember(
        channel_id=channel.id,
        user_id=current_user.id,
        role=ChannelRole.ADMIN
    )
    db.add(member)
    await db.commit()
    await db.refresh(channel)
    
    return channel

@router.get("", response_model=List[ChannelResponse])
async def list_channels(
    workspace_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all channels in a workspace."""
    result = await db.execute(
        select(Channel).where(Channel.workspace_id == workspace_id)
    )
    channels = result.scalars().all()
    return channels

@router.get("/{channel_id}", response_model=ChannelResponse)
async def get_channel(
    channel_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get channel details."""
    result = await db.execute(select(Channel).where(Channel.id == channel_id))
    channel = result.scalar_one_or_none()
    
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    return channel

@router.post("/{channel_id}/members")
async def add_channel_member(
    channel_id: str,
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Add a member to a channel."""
    member = ChannelMember(
        channel_id=channel_id,
        user_id=user_id,
        role=ChannelRole.MEMBER
    )
    db.add(member)
    await db.commit()
    
    return {"status": "added"}
