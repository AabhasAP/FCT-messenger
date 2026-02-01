from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.postgresql import Base
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class Bot(Base):
    __tablename__ = "bots"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    workspace_id = Column(String, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    token_hash = Column(String, nullable=False)  # Hashed bot token
    avatar_url = Column(String, nullable=True)
    scopes = Column(JSON, default=list)  # List of permission scopes
    created_by = Column(String, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    workspace = relationship("Workspace", back_populates="bots")
    webhooks = relationship("Webhook", back_populates="bot", cascade="all, delete-orphan")


class Webhook(Base):
    __tablename__ = "webhooks"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    workspace_id = Column(String, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    bot_id = Column(String, ForeignKey("bots.id", ondelete="CASCADE"), nullable=True)
    channel_id = Column(String, ForeignKey("channels.id", ondelete="CASCADE"), nullable=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    secret = Column(String, nullable=True)  # Webhook secret for signature verification
    events = Column(JSON, default=list)  # List of events to trigger webhook
    is_active = Column(String, default="true")  # SQLite compatibility
    created_by = Column(String, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    bot = relationship("Bot", back_populates="webhooks")


class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    workspace_id = Column(String, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action = Column(String, nullable=False)  # e.g., "channel.create", "message.delete"
    resource_type = Column(String, nullable=False)  # e.g., "channel", "message"
    resource_id = Column(String, nullable=True)
    metadata = Column(JSON, default=dict)  # Additional context
    ip_address = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
