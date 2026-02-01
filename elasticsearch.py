from elasticsearch import AsyncElasticsearch
from app.core.config import settings
from typing import Optional

class ElasticsearchClient:
    client: Optional[AsyncElasticsearch] = None
    
    @classmethod
    async def connect(cls):
        """Connect to Elasticsearch."""
        cls.client = AsyncElasticsearch(
            [f"http://{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}"],
            max_retries=3,
            retry_on_timeout=True
        )
        # Test connection
        await cls.client.ping()
        print("✓ Connected to Elasticsearch")
    
    @classmethod
    async def close(cls):
        """Close Elasticsearch connection."""
        if cls.client:
            await cls.client.close()
            print("✓ Closed Elasticsearch connection")
    
    @classmethod
    def get_client(cls) -> AsyncElasticsearch:
        """Get Elasticsearch client instance."""
        if not cls.client:
            raise RuntimeError("Elasticsearch not connected")
        return cls.client


def get_elasticsearch() -> AsyncElasticsearch:
    """Get Elasticsearch client."""
    return ElasticsearchClient.get_client()


async def init_elasticsearch():
    """Initialize Elasticsearch and create index."""
    await ElasticsearchClient.connect()
    es = ElasticsearchClient.get_client()
    
    # Create messages index if it doesn't exist
    index_name = settings.ELASTICSEARCH_INDEX
    
    if not await es.indices.exists(index=index_name):
        await es.indices.create(
            index=index_name,
            body={
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0,
                    "analysis": {
                        "analyzer": {
                            "message_analyzer": {
                                "type": "custom",
                                "tokenizer": "standard",
                                "filter": ["lowercase", "stop", "snowball"]
                            }
                        }
                    }
                },
                "mappings": {
                    "properties": {
                        "message_id": {"type": "keyword"},
                        "workspace_id": {"type": "keyword"},
                        "channel_id": {"type": "keyword"},
                        "dm_id": {"type": "keyword"},
                        "user_id": {"type": "keyword"},
                        "content": {
                            "type": "text",
                            "analyzer": "message_analyzer"
                        },
                        "created_at": {"type": "date"},
                        "updated_at": {"type": "date"}
                    }
                }
            }
        )
        print(f"✓ Created Elasticsearch index: {index_name}")
    else:
        print(f"✓ Elasticsearch index already exists: {index_name}")
