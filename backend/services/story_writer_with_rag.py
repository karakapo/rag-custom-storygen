from langchain_google_genai import ChatGoogleGenerativeAI
import os 
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import json
from dotenv import load_dotenv
import asyncio
from rag.retriever import retrieve_story_components

load_dotenv()

llm_for_writing = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.8,
    convert_system_message_to_human=True
)


prompt_for_creation = ChatPromptTemplate.from_messages([
    ("system", """Sen bir Türk hikâye anlatıcısı olan yapay zekâsın. Görevin, aşağıdaki unsurlara dayanarak etkileyici, ayrıntılı ve sürükleyici bir hikâye yazmaktır.

Yönergeler:

    Kullanıcının verdiği bileşenlere sıkı sıkıya bağlı kal ve hikâyenin açık bir yapısı olsun: başlangıç, gelişme ve sonuç.

    Mekân, ton ve türe uygun olmalı.

    Tüm olay örgüsü unsurlarını mantıklı ve uyumlu şekilde birleştir.

    Canlı, betimleyici ve duygusal olarak etkileyici bir üslupla yaz.

    Hikâye tutarlı kaldığı sürece yaratıcı sürprizler veya zenginleştirici ögeler ekleyebilirsin.

ÖNEMLİ: SADECE hikâye metnini döndür. Açıklama, başlık veya ek formatlama EKLEME. Sadece doğrudan hikâyeyi yaz."""),
("human", "Bu hikaye bileşenlerini kullanarak hikâyeyi oluştur:\n{input}")
])


async def create_story(prompt_request):
    components = await retrieve_story_components(prompt_request.prompt)
    story_writer_chain = LLMChain(
        llm=llm_for_writing,
        prompt=prompt_for_creation,
        output_key="story"
    )
    
    # Convert components to string if it's not already
    if not isinstance(components, str):
        components = str(components)
    
    # Use invoke instead of run (as per deprecation warning)
    story_text = await asyncio.to_thread(
        lambda: story_writer_chain.invoke({"input": components})["story"]
    )
    
    # Return the story text directly
    return {"content": story_text.strip()} 