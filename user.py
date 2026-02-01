from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.postgresql import Base
import enum
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class UserRole(str, enum.Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    GUEST = "guest"


class PresenceStatus(str, enum.Enum):
    ONLINE = "online"
    AWAY = "away"
    OFFLINE = "offline"


class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=True)  # Nullable for OAuth users
    full_name = Column(String, nullable=False)
    avatar_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    oauth_provider = Column(String, nullable=True)  # google, github, etc.
    oauth_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    workspaces = relationship("UserWorkspace", back_populates="user", cascade="all, delete-orphan")
    presence = relationship("UserPresence", back_populates="user", uselist=False, cascade="all, delete-orphan")


class UserWorkspace(Base):
    __tablename__ = "user_workspaces"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    workspace_id = Column(String, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.MEMBER, nullable=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="workspaces")
    workspace = relationship("Workspace", back_populates="members")
    
    __table_args__ = (
        {"sqlite_autoincrement": True},
    )


class UserPresence(Base):
    __tablename__ = "user_presence"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    status = Column(SQLEnum(PresenceStatus), default=PresenceStatus.OFFLINE, nullable=False)
    last_seen = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    custom_status = Column(String, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="presence")
