import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()


# Initialize LangChain with Gemini
llm_for_optimization = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3
)



def optimize_prompt_text(name: str, age: int, genre: str, prompt: str) -> str:
    
    optimization_template = ChatPromptTemplate.from_messages([
    ("system", """Sen bir yapay zekâ sistemleri için uzman bir prompt (istem) geliştiricisisin. Görevin, kullanıcı istemlerini şu şekilde geliştirmektir:

    Yazım ve dilbilgisi hatalarını düzeltmek
    İstemi daha ayrıntılı ve özgül hâle getirmek
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

    optimization_chain = LLMChain(
        llm=llm_for_optimization,
        prompt=optimization_template,
        output_key="optimized_prompt"
)
    
    result = optimization_chain.run({
        "name": name,
        "age": age,
        "genre": genre,
        "prompt": prompt
    })
    return result