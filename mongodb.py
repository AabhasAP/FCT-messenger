from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from typing import Optional

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    
    @classmethod
    async def connect(cls):
        """Connect to MongoDB."""
        cls.client = AsyncIOMotorClient(settings.MONGODB_URL)
        # Test connection
        await cls.client.admin.command('ping')
        print("✓ Connected to MongoDB")
    
    @classmethod
    async def close(cls):
        """Close MongoDB connection."""
        if cls.client:
            cls.client.close()
            print("✓ Closed MongoDB connection")
    
    @classmethod
    def get_database(cls):
        """Get database instance."""
        if not cls.client:
            raise RuntimeError("MongoDB not connected")
        return cls.client[settings.MONGODB_DB]
    
    @classmethod
    def get_collection(cls, name: str):
        """Get collection by name."""
        db = cls.get_database()
        return db[name]


# Convenience function
def get_mongo_db():
    """Get MongoDB database instance."""
    return MongoDB.get_database()


async def init_mongodb():
    """Initialize MongoDB collections and indexes."""
    await MongoDB.connect()
    db = MongoDB.get_database()
    
    # Messages collection
    messages = db.messages
    await messages.create_index([("workspace_id", 1), ("channel_id", 1), ("created_at", -1)])
    await messages.create_index([("workspace_id", 1), ("dm_id", 1), ("created_at", -1)])
    await messages.create_index([("thread_id", 1), ("created_at", 1)])
    await messages.create_index([("user_id", 1)])
    
    # Threads collection
    threads = db.threads
    await threads.create_index([("parent_message_id", 1)])
    
    print("✓ MongoDB indexes created")
