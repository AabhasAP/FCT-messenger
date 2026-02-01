from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from app.db.postgresql import get_db
from app.models.bot import Bot, Webhook
from app.models.user import User
from app.core.security import generate_bot_token, hash_bot_token
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()

class BotCreate(BaseModel):
    workspace_id: str
    name: str
    description: Optional[str] = None
    scopes: List[str] = []

class BotResponse(BaseModel):
    id: str
    workspace_id: str
    name: str
    description: Optional[str]
    scopes: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class BotTokenResponse(BaseModel):
    bot_id: str
    token: str

@router.post("", response_model=BotTokenResponse, status_code=201)
async def create_bot(
    bot_data: BotCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new bot."""
    # Generate bot token
    token = generate_bot_token()
    token_hash = hash_bot_token(token)
    
    bot = Bot(
        workspace_id=bot_data.workspace_id,
        name=bot_data.name,
        description=bot_data.description,
        token_hash=token_hash,
        scopes=bot_data.scopes,
        created_by=current_user.id
    )
    db.add(bot)
    await db.commit()
    await db.refresh(bot)
    
    return BotTokenResponse(bot_id=bot.id, token=token)

@router.get("", response_model=List[BotResponse])
async def list_bots(
    workspace_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all bots in a workspace."""
    result = await db.execute(
        select(Bot).where(Bot.workspace_id == workspace_id)
    )
    bots = result.scalars().all()
    return bots

@router.post("/{bot_id}/regenerate-token", response_model=BotTokenResponse)
async def regenerate_bot_token(
    bot_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Regenerate bot token."""
    result = await db.execute(select(Bot).where(Bot.id == bot_id))
    bot = result.scalar_one_or_none()
    
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    # Generate new token
    token = generate_bot_token()
    bot.token_hash = hash_bot_token(token)
    
    await db.commit()
    
    return BotTokenResponse(bot_id=bot.id, token=token)
