import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

from core.config import settings


# Initialize LangChain with Gemini
llm_for_optimization = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=settings.GOOGLE_API_KEY,
    temperature=0.3
)



def optimize_prompt_text(name: str, age: int, genre: str, prompt: str) -> str:
    
    optimization_template = ChatPromptTemplate.from_messages([
    ("system", """Sen bir yapay zekâ sistemleri için uzman bir prompt (istem) geliştiricisisin. 
    Görevin, kullanıcı istemlerini şu şekilde geliştirmektir:

    Yazım ve dilbilgisi hatalarını düzeltmek
    Yapay zekânın daha iyi anlayacağı şekilde optimize etmek
    Orijinal amacı koruyarak netliği artırmak
    Eksikse gerekli bağlamı eklemek
    İstemin şu özelliklere sahip olmasına odaklan:
    Açık ve belirsizlikten uzak
    İyi yapılandırılmış
    Özgül ve ayrıntılı
    Hatalardan arınmış
    Yapay zekâ tarafından kolayca anlaşılır şekilde optimize edilmiş"""),
    ("human", """
    Lütfen bu istemi yapay zekânın daha iyi anlayacağı şekilde optimize et:
    Karakter Adı: {name}
    Karakter Yaşı: {age}
    Tür: {genre}
    İstem: {prompt}
    """)
])

    # Modern LangChain syntax using RunnableSequence
    optimization_chain = optimization_template | llm_for_optimization
    
    result = optimization_chain.invoke({
        "name": name,
        "age": age,
        "genre": genre,
        "prompt": prompt
    })
    return result.content