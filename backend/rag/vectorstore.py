from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client.models import PointStruct
import os 
import uuid 
import json 



URL = os.getenv("QDRANT_URL")  
API_KEY = os.getenv("QDRANT_KEY")            


client = QdrantClient(url=URL, api_key=API_KEY)


embedding_model = SentenceTransformer('all-MiniLM-L6-v2')




def get_embedding(text):
    return embedding_model.encode(text)


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