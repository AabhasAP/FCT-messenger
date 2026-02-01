# MongoDB schemas (document structure)
# These are not SQLAlchemy models but Python dataclasses for type hints

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Reaction(BaseModel):
    emoji: str
    user_ids: List[str] = []
    count: int = 0


class Attachment(BaseModel):
    file_id: str
    filename: str
    file_type: str
    file_size: int
    url: str
    preview_url: Optional[str] = None


class Message(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    workspace_id: str
    channel_id: Optional[str] = None
    dm_id: Optional[str] = None
    user_id: str
    content: str  # Encrypted content
    thread_id: Optional[str] = None
    parent_message_id: Optional[str] = None
    attachments: List[Attachment] = []
    reactions: List[Reaction] = []
    is_edited: bool = False
    is_deleted: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Thread(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    parent_message_id: str
    workspace_id: str
    channel_id: Optional[str] = None
    dm_id: Optional[str] = None
    reply_count: int = 0
    participant_ids: List[str] = []
    last_reply_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
