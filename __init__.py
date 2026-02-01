# Import all models to ensure they're registered with SQLAlchemy
from app.models.user import User, UserWorkspace, UserPresence, UserRole, PresenceStatus
from app.models.workspace import Workspace, WorkspaceInvite
from app.models.channel import Channel, ChannelMember, DirectMessage, ChannelType, ChannelRole
from app.models.bot import Bot, Webhook, AuditLog
from app.models.message import Message, Thread, Reaction, Attachment

__all__ = [
    "User",
    "UserWorkspace",
    "UserPresence",
    "UserRole",
    "PresenceStatus",
    "Workspace",
    "WorkspaceInvite",
    "Channel",
    "ChannelMember",
    "DirectMessage",
    "ChannelType",
    "ChannelRole",
    "Bot",
    "Webhook",
    "AuditLog",
    "Message",
    "Thread",
    "Reaction",
    "Attachment",
]
