from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv
from services.prompt_optimizer import optimize_prompt_text

load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7  
)

# Create story writing template
story_template = ChatPromptTemplate.from_messages([
    ("system", """Sen özgünlük ve duygusal derinliğe odaklanan yaratıcı bir hikâye yazarı olan yapay zekâsın.
Görevin, aşağıdaki özellikleri taşıyan bir hikâye yazmaktır:

    Tamamen özgün ve yaratıcı olması
    Derinlemesine karakter gelişimi içermesi
    Beklenmedik olay örgüsü dönüşleri barındırması
    Güçlü duygular uyandırması
    Akılda kalıcı ve sürükleyici olması"""),
    ("human", """
    Bu optimize edilmiş isteme dayalı olarak yaratıcı ve özgün bir hikâye yaz:

    {optimized_prompt}

    Yönergeler:

    Yaratıcı ve özgün ol
    Belirli bir şablonu takip etme
    Karakter gelişimine ve duygusal derinliğe odaklan
    Beklenmedik olay örgüsü dönüşleri yarat
    Hikâyeyi sürükleyici ve unutulmaz kıl
    Sadece hikâye metnini döndür, ek bir metin yazma.
""")
])


story_chain = LLMChain(
    llm=llm,
    prompt=story_template,
    output_key="story"
)


def write_story_with_optimization(user_prompt: str) -> dict:
    """
    Optimizes the user's prompt and generates a story using SequentialChain.
    
    Args:
        user_prompt (str): The original prompt from the user
        
    Returns:
        dict: A dictionary containing both the optimized prompt and the generated story
    """

    optimized_prompt = optimize_prompt_text(user_prompt)

    result = story_chain({"optimized_prompt": optimized_prompt})
    return {
        "story": result["story"].strip()
    } 