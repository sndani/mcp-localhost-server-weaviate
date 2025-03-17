import weaviate
import weaviate.classes as wvc
from weaviate.auth import Auth
import os
from typing import Optional
from weaviate.client import WeaviateClient
from weaviate.connect import ConnectionParams, ProtocolParams

def create_collections(
    weaviate_url: Optional[str],
    weaviate_api_key: Optional[str],
    search_collection_name: str,
    store_collection_name: str,
    openai_api_key: Optional[str] = None,
    cohere_api_key: Optional[str] = None
):
    """
    Create the collections needed for the Weaviate functionality.
    """
    # Set up headers for vectorization
    headers = {}
    if openai_api_key:
        headers["X-OpenAI-Api-Key"] = openai_api_key
    if cohere_api_key:
        headers["X-Cohere-Api-Key"] = cohere_api_key

    # Direct client creation with connection parameters
    client = WeaviateClient(
        connection_params=ConnectionParams(
            http=ProtocolParams(host="localhost", port=8080, secure=False),
            grpc=ProtocolParams(host="localhost", port=50051, secure=False),
        ),
        additional_headers=headers,
    )
    
    print(client.is_ready())
    
    # Delete existing collections if they exist
    for collection_name in [search_collection_name, store_collection_name]:
        if client.collections.exists(collection_name):
            client.collections.delete(collection_name)

    # Create search collection for knowledge base
    search_collection = client.collections.create(
        name=search_collection_name,
        properties=[
            wvc.config.Property(
                name="content",
                data_type=wvc.config.DataType.TEXT,
                description="The content of the knowledge base entry"
            )
        ]
    )

    # Create store collection for memories
    store_collection = client.collections.create(
        name=store_collection_name,
        properties=[
            wvc.config.Property(
                name="content",
                data_type=wvc.config.DataType.TEXT,
                description="The content of the stored memory"
            )
        ]
    )

    client.close()

if __name__ == "__main__":
    # Get configuration from environment variables
    weaviate_url = os.getenv("WEAVIATE_URL")
    weaviate_api_key = os.getenv("WEAVIATE_API_KEY")
    search_collection_name = os.getenv("SEARCH_COLLECTION_NAME")
    store_collection_name = os.getenv("STORE_COLLECTION_NAME")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    cohere_api_key = os.getenv("COHERE_API_KEY")

    if not search_collection_name or not store_collection_name:
        raise ValueError("Collection names must be provided")
    
    if not (openai_api_key or cohere_api_key):
        raise ValueError("Either OpenAI or Cohere API key must be provided")

    create_collections(
        weaviate_url,
        weaviate_api_key,
        search_collection_name,
        store_collection_name,
        openai_api_key,
        cohere_api_key
    )
