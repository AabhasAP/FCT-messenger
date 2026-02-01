from typing import Dict, Set, Optional
from fastapi import WebSocket
import json
import asyncio
from datetime import datetime
from app.db.redis import get_redis
from app.core.config import settings


class ConnectionManager:
    """Manage WebSocket connections with Redis pub/sub for scaling."""
    
    def __init__(self):
        # workspace_id -> set of WebSocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        # websocket -> user_id mapping
        self.connection_users: Dict[WebSocket, str] = {}
        # websocket -> workspace_id mapping
        self.connection_workspaces: Dict[WebSocket, str] = {}
        self.redis = None
        self.pubsub = None
        self.listener_task = None
    
    async def initialize(self):
        """Initialize Redis pub/sub."""
        self.redis = get_redis()
        self.pubsub = self.redis.pubsub()
        await self.pubsub.subscribe("websocket_events")
        # Start listening for Redis messages
        self.listener_task = asyncio.create_task(self._redis_listener())
    
    async def connect(self, websocket: WebSocket, workspace_id: str, user_id: str):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        
        if workspace_id not in self.active_connections:
            self.active_connections[workspace_id] = set()
        
        self.active_connections[workspace_id].add(websocket)
        self.connection_users[websocket] = user_id
        self.connection_workspaces[websocket] = workspace_id
        
        print(f"✓ User {user_id} connected to workspace {workspace_id}")
    
    async def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        workspace_id = self.connection_workspaces.get(websocket)
        user_id = self.connection_users.get(websocket)
        
        if workspace_id and websocket in self.active_connections.get(workspace_id, set()):
            self.active_connections[workspace_id].remove(websocket)
            
            # Clean up empty workspace sets
            if not self.active_connections[workspace_id]:
                del self.active_connections[workspace_id]
        
        self.connection_users.pop(websocket, None)
        self.connection_workspaces.pop(websocket, None)
        
        if user_id and workspace_id:
            print(f"✓ User {user_id} disconnected from workspace {workspace_id}")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send a message to a specific WebSocket connection."""
        try:
            await websocket.send_json(message)
        except Exception as e:
            print(f"Error sending message: {e}")
            await self.disconnect(websocket)
    
    async def broadcast_to_workspace(self, workspace_id: str, message: dict, exclude: Optional[WebSocket] = None):
        """Broadcast a message to all connections in a workspace."""
        if workspace_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[workspace_id]:
                if connection != exclude:
                    try:
                        await connection.send_json(message)
                    except Exception as e:
                        print(f"Error broadcasting: {e}")
                        disconnected.append(connection)
            
            # Clean up disconnected connections
            for conn in disconnected:
                await self.disconnect(conn)
    
    async def broadcast_to_channel(self, workspace_id: str, channel_id: str, message: dict):
        """Broadcast a message to all users in a specific channel."""
        # In a real implementation, you'd check channel membership
        # For now, broadcast to entire workspace
        await self.broadcast_to_workspace(workspace_id, message)
    
    async def publish_event(self, event: dict):
        """Publish an event to Redis for other server instances."""
        if self.redis:
            await self.redis.publish("websocket_events", json.dumps(event))
    
    async def _redis_listener(self):
        """Listen for events from Redis pub/sub."""
        try:
            async for message in self.pubsub.listen():
                if message["type"] == "message":
                    try:
                        event = json.loads(message["data"])
                        workspace_id = event.get("workspace_id")
                        if workspace_id:
                            await self.broadcast_to_workspace(workspace_id, event)
                    except json.JSONDecodeError:
                        pass
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Redis listener error: {e}")
    
    async def send_typing_indicator(self, workspace_id: str, channel_id: str, user_id: str, is_typing: bool):
        """Send typing indicator to channel."""
        message = {
            "type": "typing.update",
            "channel_id": channel_id,
            "user_id": user_id,
            "is_typing": is_typing,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.broadcast_to_channel(workspace_id, channel_id, message)
    
    async def send_presence_update(self, workspace_id: str, user_id: str, status: str):
        """Send presence update to workspace."""
        message = {
            "type": "presence.updated",
            "user_id": user_id,
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.broadcast_to_workspace(workspace_id, message)
    
    def get_workspace_connection_count(self, workspace_id: str) -> int:
        """Get number of active connections for a workspace."""
        return len(self.active_connections.get(workspace_id, set()))


# Global connection manager instance
manager = ConnectionManager()
