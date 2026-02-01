# WebSocket Event Specifications

## Connection

### Endpoint
```
ws://localhost:8000/ws/{workspace_id}?token={access_token}
```

### Connection Flow
1. Client connects with workspace ID and access token
2. Server validates token and accepts connection
3. Server sends initial state (if needed)
4. Client and server exchange heartbeat pings

## Event Format

All WebSocket messages follow this format:

```json
{
  "type": "event.name",
  "data": { ... },
  "workspace_id": "workspace-uuid",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

## Client → Server Events

### Ping (Heartbeat)
```json
{
  "type": "ping"
}
```

**Response:**
```json
{
  "type": "pong"
}
```

### Typing Indicator
```json
{
  "type": "typing",
  "channel_id": "channel-uuid",
  "is_typing": true
}
```

## Server → Client Events

### Message Events

#### message.new
New message sent to a channel or DM.

```json
{
  "type": "message.new",
  "data": {
    "id": "message-uuid",
    "channel_id": "channel-uuid",
    "user_id": "user-uuid",
    "content": "Hello, world!",
    "attachments": [],
    "reactions": [],
    "created_at": "2024-01-01T12:00:00.000Z"
  },
  "workspace_id": "workspace-uuid",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

#### message.updated
Message edited.

```json
{
  "type": "message.updated",
  "data": {
    "id": "message-uuid",
    "content": "Updated content",
    "updated_at": "2024-01-01T12:05:00.000Z"
  },
  "workspace_id": "workspace-uuid",
  "timestamp": "2024-01-01T12:05:00.000Z"
}
```

#### message.deleted
Message deleted.

```json
{
  "type": "message.deleted",
  "data": {
    "id": "message-uuid",
    "deleted_at": "2024-01-01T12:10:00.000Z"
  },
  "workspace_id": "workspace-uuid",
  "timestamp": "2024-01-01T12:10:00.000Z"
}
```

### Reaction Events

#### reaction.added
Reaction added to a message.

```json
{
  "type": "reaction.added",
  "data": {
    "message_id": "message-uuid",
    "emoji": "👍",
    "user_id": "user-uuid"
  },
  "workspace_id": "workspace-uuid",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

#### reaction.removed
Reaction removed from a message.

```json
{
  "type": "reaction.removed",
  "data": {
    "message_id": "message-uuid",
    "emoji": "👍",
    "user_id": "user-uuid"
  },
  "workspace_id": "workspace-uuid",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### Typing Events

#### typing.start
User started typing.

```json
{
  "type": "typing.start",
  "data": {
    "channel_id": "channel-uuid",
    "user_id": "user-uuid"
  },
  "workspace_id": "workspace-uuid",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

#### typing.stop
User stopped typing.

```json
{
  "type": "typing.stop",
  "data": {
    "channel_id": "channel-uuid",
    "user_id": "user-uuid"
  },
  "workspace_id": "workspace-uuid",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### Presence Events

#### presence.updated
User presence status changed.

```json
{
  "type": "presence.updated",
  "data": {
    "user_id": "user-uuid",
    "status": "online"
  },
  "workspace_id": "workspace-uuid",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

**Status values:** `online`, `away`, `offline`

### Channel Events

#### channel.created
New channel created.

```json
{
  "type": "channel.created",
  "data": {
    "id": "channel-uuid",
    "name": "general",
    "type": "public",
    "created_by": "user-uuid"
  },
  "workspace_id": "workspace-uuid",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

#### channel.updated
Channel updated.

```json
{
  "type": "channel.updated",
  "data": {
    "id": "channel-uuid",
    "name": "new-name",
    "description": "Updated description"
  },
  "workspace_id": "workspace-uuid",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

#### channel.deleted
Channel deleted.

```json
{
  "type": "channel.deleted",
  "data": {
    "id": "channel-uuid"
  },
  "workspace_id": "workspace-uuid",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### Member Events

#### member.joined
User joined a channel.

```json
{
  "type": "member.joined",
  "data": {
    "channel_id": "channel-uuid",
    "user_id": "user-uuid"
  },
  "workspace_id": "workspace-uuid",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

#### member.left
User left a channel.

```json
{
  "type": "member.left",
  "data": {
    "channel_id": "channel-uuid",
    "user_id": "user-uuid"
  },
  "workspace_id": "workspace-uuid",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### Thread Events

#### thread.updated
Thread reply count or participants updated.

```json
{
  "type": "thread.updated",
  "data": {
    "parent_message_id": "message-uuid",
    "reply_count": 5,
    "last_reply_at": "2024-01-01T12:00:00.000Z"
  },
  "workspace_id": "workspace-uuid",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### Error Events

#### error
Error occurred during WebSocket communication.

```json
{
  "type": "error",
  "data": {
    "message": "Error description",
    "code": "ERROR_CODE"
  },
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

## Error Codes

- `INVALID_TOKEN` - Authentication token is invalid
- `UNAUTHORIZED` - User not authorized for this workspace
- `RATE_LIMITED` - Too many requests
- `INTERNAL_ERROR` - Server error

## Best Practices

1. **Heartbeat** - Send ping every 30 seconds to keep connection alive
2. **Reconnection** - Implement exponential backoff for reconnection attempts
3. **Event Buffering** - Buffer events during disconnection and sync on reconnect
4. **Error Handling** - Always handle error events gracefully
5. **Typing Indicators** - Debounce typing events to avoid spam
