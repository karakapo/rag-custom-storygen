from vectorstore import client, collection_name

def recreate_collection():
    # Koleksiyon varsa sil
    if client.collection_exists(collection_name):
        print(f"Deleting existing collection: {collection_name}")
        client.delete_collection(collection_name)
    
    # Yeni koleksiyon oluştur
    print(f"Creating new collection: {collection_name}")
    client.create_collection(
        collection_name=collection_name,
        vectors_config={"size": 384, "distance": "Cosine"},
    )
    
    # Category için index oluştur
    print("Creating index for category field")
    client.create_payload_index(
        collection_name=collection_name,
        field_name="category",
        field_schema="keyword"
    )
    
    print("Collection recreated successfully!")

if __name__ == "__main__":
    recreate_collection() 