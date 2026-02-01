from enum import Enum
from typing import Any, Dict
from datetime import datetime


class WSEventType(str, Enum):
    """WebSocket event types."""
    # Messages
    MESSAGE_NEW = "message.new"
    MESSAGE_UPDATED = "message.updated"
    MESSAGE_DELETED = "message.deleted"
    
    # Reactions
    REACTION_ADDED = "reaction.added"
    REACTION_REMOVED = "reaction.removed"
    
    # Typing
    TYPING_START = "typing.start"
    TYPING_STOP = "typing.stop"
    
    # Presence
    PRESENCE_UPDATED = "presence.updated"
    
    # Channels
    CHANNEL_CREATED = "channel.created"
    CHANNEL_UPDATED = "channel.updated"
    CHANNEL_DELETED = "channel.deleted"
    
    # Members
    MEMBER_JOINED = "member.joined"
    MEMBER_LEFT = "member.left"
    
    # Threads
    THREAD_UPDATED = "thread.updated"
    
    # System
    HEARTBEAT = "heartbeat"
    ERROR = "error"


def create_event(event_type: WSEventType, data: Dict[str, Any], workspace_id: str = None) -> Dict[str, Any]:
    """Create a standardized WebSocket event."""
    return {
        "type": event_type.value,
        "data": data,
        "workspace_id": workspace_id,
        "timestamp": datetime.utcnow().isoformat()
    }


def create_message_event(message: Dict[str, Any], workspace_id: str) -> Dict[str, Any]:
    """Create a new message event."""
    return create_event(WSEventType.MESSAGE_NEW, message, workspace_id)


def create_reaction_event(message_id: str, emoji: str, user_id: str, action: str, workspace_id: str) -> Dict[str, Any]:
    """Create a reaction event."""
    event_type = WSEventType.REACTION_ADDED if action == "add" else WSEventType.REACTION_REMOVED
    return create_event(
        event_type,
        {
            "message_id": message_id,
            "emoji": emoji,
            "user_id": user_id
        },
        workspace_id
    )


def create_typing_event(channel_id: str, user_id: str, is_typing: bool, workspace_id: str) -> Dict[str, Any]:
    """Create a typing indicator event."""
    event_type = WSEventType.TYPING_START if is_typing else WSEventType.TYPING_STOP
    return create_event(
        event_type,
        {
            "channel_id": channel_id,
            "user_id": user_id
        },
        workspace_id
    )


def create_presence_event(user_id: str, status: str, workspace_id: str) -> Dict[str, Any]:
    """Create a presence update event."""
    return create_event(
        WSEventType.PRESENCE_UPDATED,
        {
            "user_id": user_id,
            "status": status
        },
        workspace_id
    )


def create_channel_event(event_type: WSEventType, channel: Dict[str, Any], workspace_id: str) -> Dict[str, Any]:
    """Create a channel event."""
    return create_event(event_type, channel, workspace_id)


def create_error_event(error_message: str, error_code: str = None) -> Dict[str, Any]:
    """Create an error event."""
    return create_event(
        WSEventType.ERROR,
        {
            "message": error_message,
            "code": error_code
        }
    )
