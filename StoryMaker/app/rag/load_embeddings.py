from vector_store import client
import json
from pathlib import Path
from rag.embedder import get_embedding
import uuid
from qdrant_client.models import PointStruct

    
def save_to_qdrant(category, name, content):
    
    embedding = get_embedding(content)
    
    point = PointStruct(
        id=str(uuid.uuid4()) ,
        vector=embedding,
        payload={"category": category,
                  "name": name,
                  "content" : content}
    )
    
    client.upsert(
        collection_name="story_companents",
        points=[point]  
    )


    
def save_data(json_path):
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)


    for item in data:
        save_to_qdrant(
            category=item["category"],
            name=item["name"],
            content=item["content"]
        )