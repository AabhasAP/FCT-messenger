from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from app.db.elasticsearch import get_elasticsearch
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user
from app.core.config import settings

router = APIRouter()

class SearchResult(BaseModel):
    message_id: str
    content: str
    channel_id: str
    user_id: str
    created_at: str
    score: float

@router.get("/messages", response_model=List[SearchResult])
async def search_messages(
    query: str,
    workspace_id: str,
    channel_id: str = None,
    limit: int = 20,
    current_user: User = Depends(get_current_user)
):
    """Search messages using Elasticsearch."""
    es = get_elasticsearch()
    
    search_query = {
        "bool": {
            "must": [
                {"match": {"content": query}},
                {"term": {"workspace_id": workspace_id}}
            ]
        }
    }
    
    if channel_id:
        search_query["bool"]["must"].append({"term": {"channel_id": channel_id}})
    
    result = await es.search(
        index=settings.ELASTICSEARCH_INDEX,
        body={
            "query": search_query,
            "size": limit,
            "sort": [{"created_at": {"order": "desc"}}]
        }
    )
    
    hits = result["hits"]["hits"]
    return [
        SearchResult(
            message_id=hit["_source"]["message_id"],
            content=hit["_source"]["content"],
            channel_id=hit["_source"].get("channel_id", ""),
            user_id=hit["_source"]["user_id"],
            created_at=hit["_source"]["created_at"],
            score=hit["_score"]
        )
        for hit in hits
    ]
