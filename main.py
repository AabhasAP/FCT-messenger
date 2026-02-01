from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from prometheus_client import make_asgi_app
import uvicorn

from app.core.config import settings
from app.db.postgresql import init_db
from app.db.mongodb import init_mongodb
from app.db.redis import init_redis, RedisClient
from app.db.elasticsearch import init_elasticsearch, ElasticsearchClient
from app.websocket.connection_manager import manager
from app.api.v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    print("🚀 Starting Forensic Cyber Tech Cloud Messenger...")
    
    try:
        # Initialize databases
        await init_db()
        await init_mongodb()
        await init_redis()
        await init_elasticsearch()
        
        # Initialize WebSocket manager
        await manager.initialize()
        
        print("✅ All services initialized successfully")
        
        yield
        
    finally:
        # Shutdown
        print("🛑 Shutting down...")
        await RedisClient.close()
        await ElasticsearchClient.close()
        print("✅ Cleanup complete")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# Prometheus metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.websocket("/ws/{workspace_id}")
async def websocket_endpoint(websocket: WebSocket, workspace_id: str, token: str = None):
    """WebSocket endpoint for real-time communication."""
    # In production, validate token and extract user_id
    # For now, accept the connection
    user_id = "demo_user"  # Extract from token in production
    
    await manager.connect(websocket, workspace_id, user_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            
            # Handle different message types
            msg_type = data.get("type")
            
            if msg_type == "ping":
                await manager.send_personal_message({"type": "pong"}, websocket)
            
            elif msg_type == "typing":
                channel_id = data.get("channel_id")
                is_typing = data.get("is_typing", True)
                await manager.send_typing_indicator(workspace_id, channel_id, user_id, is_typing)
            
            else:
                # Echo back for now (in production, process and broadcast)
                await manager.broadcast_to_workspace(workspace_id, data, exclude=websocket)
    
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        await manager.disconnect(websocket)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
