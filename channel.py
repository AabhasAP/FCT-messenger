from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.postgresql import Base
import enum
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class ChannelType(str, enum.Enum):
    PUBLIC = "public"
    PRIVATE = "private"


class ChannelRole(str, enum.Enum):
    ADMIN = "admin"
    MEMBER = "member"


class Channel(Base):
    __tablename__ = "channels"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    workspace_id = Column(String, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    type = Column(SQLEnum(ChannelType), default=ChannelType.PUBLIC, nullable=False)
    created_by = Column(String, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    workspace = relationship("Workspace", back_populates="channels")
    members = relationship("ChannelMember", back_populates="channel", cascade="all, delete-orphan")


class ChannelMember(Base):
    __tablename__ = "channel_members"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    channel_id = Column(String, ForeignKey("channels.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(SQLEnum(ChannelRole), default=ChannelRole.MEMBER, nullable=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    channel = relationship("Channel", back_populates="members")


class DirectMessage(Base):
    __tablename__ = "direct_messages"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    workspace_id = Column(String, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    user1_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user2_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
