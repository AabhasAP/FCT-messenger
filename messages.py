from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

from app.db.mongodb import get_mongo_db
from app.models.user import User
from app.models.message import Message, Reaction, Attachment
from app.core.encryption import encryption
from app.api.v1.endpoints.auth import get_current_user
from app.websocket.connection_manager import manager
from app.websocket.events import create_message_event

router = APIRouter()

class MessageCreate(BaseModel):
    channel_id: Optional[str] = None
    dm_id: Optional[str] = None
    content: str
    thread_id: Optional[str] = None
    attachments: List[Attachment] = []

class MessageResponse(BaseModel):
    id: str
    workspace_id: str
    channel_id: Optional[str]
    dm_id: Optional[str]
    user_id: str
    content: str
    thread_id: Optional[str]
    attachments: List[Attachment]
    reactions: List[Reaction]
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.post("", response_model=MessageResponse, status_code=201)
async def create_message(
    message_data: MessageCreate,
    workspace_id: str,
    current_user: User = Depends(get_current_user)
):
    """Send a new message."""
    db = get_mongo_db()
    messages_collection = db.messages
    
    # Encrypt content
    encrypted_content = encryption.encrypt(message_data.content)
    
    # Create message document
    message_doc = {
        "workspace_id": workspace_id,
        "channel_id": message_data.channel_id,
        "dm_id": message_data.dm_id,
        "user_id": current_user.id,
        "content": encrypted_content,
        "thread_id": message_data.thread_id,
        "attachments": [att.dict() for att in message_data.attachments],
        "reactions": [],
        "is_edited": False,
        "is_deleted": False,
        "created_at": datetime.utcnow()
    }
    
    result = await messages_collection.insert_one(message_doc)
    message_doc["_id"] = result.inserted_id
    
    # Decrypt for response
    message_doc["content"] = message_data.content
    message_doc["id"] = str(result.inserted_id)
    
    # Broadcast via WebSocket
    await manager.broadcast_to_workspace(
        workspace_id,
        create_message_event(message_doc, workspace_id)
    )
    
    return MessageResponse(**message_doc)

@router.get("", response_model=List[MessageResponse])
async def get_messages(
    channel_id: Optional[str] = None,
    dm_id: Optional[str] = None,
    limit: int = 50,
    before: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Get messages from a channel or DM."""
    db = get_mongo_db()
    messages_collection = db.messages
    
    query = {}
    if channel_id:
        query["channel_id"] = channel_id
    if dm_id:
        query["dm_id"] = dm_id
    if before:
        query["_id"] = {"$lt": ObjectId(before)}
    
    cursor = messages_collection.find(query).sort("created_at", -1).limit(limit)
    messages = await cursor.to_list(length=limit)
    
    # Decrypt messages
    for msg in messages:
        msg["content"] = encryption.decrypt(msg["content"])
        msg["id"] = str(msg["_id"])
    
    return [MessageResponse(**msg) for msg in messages]

@router.post("/{message_id}/reactions")
async def add_reaction(
    message_id: str,
    emoji: str,
    current_user: User = Depends(get_current_user)
):
    """Add a reaction to a message."""
    db = get_mongo_db()
    messages_collection = db.messages
    
    await messages_collection.update_one(
        {"_id": ObjectId(message_id), "reactions.emoji": emoji},
        {"$addToSet": {"reactions.$.user_ids": current_user.id}, "$inc": {"reactions.$.count": 1}}
    )
    
    # If reaction doesn't exist, add it
    await messages_collection.update_one(
        {"_id": ObjectId(message_id), "reactions.emoji": {"$ne": emoji}},
        {"$push": {"reactions": {"emoji": emoji, "user_ids": [current_user.id], "count": 1}}}
    )
    
    return {"status": "added"}
