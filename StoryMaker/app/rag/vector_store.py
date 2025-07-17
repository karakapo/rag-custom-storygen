from qdrant_client import QdrantClient
import os 
import uuid 
import json 
from core.config import settings

URL = settings.QDRANT_URL
API_KEY = settings.QDRANT_KEY


client = QdrantClient(url=URL, api_key=API_KEY)


collection_name="story_companents"

# Koleksiyon yoksa oluştur
existing_collections = [col.name for col in client.get_collections().collections]
if collection_name not in existing_collections:
    client.create_collection(
        collection_name=collection_name,
        vectors_config={"size": 384, "distance": "Cosine"},
    )
    # Category için index oluştur
    client.create_payload_index(
        collection_name=collection_name,
        field_name="category",
        field_schema="keyword"
    )
else:
    # Koleksiyon varsa ve boyut farklıysa, koleksiyonu sil ve yeniden oluştur
    collection_info = client.get_collection(collection_name)
    if collection_info.config.params.vectors.size != 384:
        client.delete_collection(collection_name)
        client.create_collection(
            collection_name=collection_name,
            vectors_config={"size": 384, "distance": "Cosine"},
        )
        # Category için index oluştur
        client.create_payload_index(
            collection_name=collection_name,
            field_name="category",
            field_schema="keyword"
        )



