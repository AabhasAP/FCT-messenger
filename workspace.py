from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.postgresql import Base
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class Workspace(Base):
    __tablename__ = "workspaces"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=True)
    icon_url = Column(String, nullable=True)
    owner_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    members = relationship("UserWorkspace", back_populates="workspace", cascade="all, delete-orphan")
    channels = relationship("Channel", back_populates="workspace", cascade="all, delete-orphan")
    invites = relationship("WorkspaceInvite", back_populates="workspace", cascade="all, delete-orphan")
    bots = relationship("Bot", back_populates="workspace", cascade="all, delete-orphan")


class WorkspaceInvite(Base):
    __tablename__ = "workspace_invites"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    workspace_id = Column(String, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    email = Column(String, nullable=False)
    token = Column(String, unique=True, nullable=False, index=True)
    invited_by = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    workspace = relationship("Workspace", back_populates="invites")
