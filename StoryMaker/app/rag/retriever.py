from rag.embedder import get_embedding
import asyncio
import random



async def retrieve_story_components(query: str, limit: int = 1):
    """
    Belirli kategorilerde paralel arama yapan fonksiyon.
    Sadece içerik (content) kısmını döndürür.
    
    Args:
        categories (list): Aranacak kategori listesi
        query (str): Arama sorgusu
        limit (int): Her kategori için döndürülecek sonuç sayısı
    
    Returns:
        sadece içerikleri döndürür.
    """ 
    vector = get_embedding(query)
    loop = asyncio.get_event_loop()
    tasks = []
    

    categories = ["Main_character","Environment","Main_conflict","Moral","Plot","character_goal","Genre","Final_type"]

    random_categories = random.choices(categories, k=4)

    for category in random_categories:
        search_params = {
            "collection_name": "story_companents",
            "query_vector": vector,
            "limit": limit,
            "with_payload": True,
            "query_filter": {
                "must": [
                    {
                        "key": "category",
                        "match": {"value": category}
                    }
                ]
            }
        }
        tasks.append(loop.run_in_executor(None, lambda: client.search(**search_params)))
    
    results = await asyncio.gather(*tasks)
    
    # Sonuçlardan sadece content kısmını al
    categorized_contents = {}
    for category, result in zip(categories, results):
        # Her bir sonuç için content'leri listeye al
        contents = [hit.payload.get('content') for hit in result if hit.payload and 'content' in hit.payload]
        categorized_contents[category] = contents[0] if contents else None
        
    return categorized_contents



