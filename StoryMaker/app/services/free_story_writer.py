from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
import os

from services.prompt_optimizer import optimize_prompt_text
from core.config import settings



llm_for_free_writing= ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=settings.GOOGLE_API_KEY,
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
   bu prompta göre yaratıcı ve özgün bir hikâye yaz:

    {optimized_prompt}

    {character_info}

    Yönergeler:

    Yaratıcı ve özgün ol
    Belirli bir şablonu takip etme
    Karakter gelişimine ve duygusal derinliğe odaklan
    Beklenmedik olay örgüsü dönüşleri yarat
    Hikâyeyi sürükleyici ve unutulmaz kıl
    Sadece hikâye metnini döndür, ek bir metin yazma.
""")
])


# Modern LangChain syntax using RunnableSequence
story_chain = story_template | llm_for_free_writing


def write_free_story(user_prompt: str, name: str = None, age: int = None, gender: str = None, genre: str = "Genel") -> dict:
    """
    Optimizes the user's prompt and generates a story using modern LangChain syntax.
    
    Args:
        user_prompt (str): The original prompt from the user
        name (str, optional): Character name
        age (int, optional): Character age
        gender (str, optional): Character gender
        
    Returns:
        dict: A dictionary containing the generated story
    """

    # Provide default values for required parameters
    name = name 
    age = age 
    genre = genre or "Genel"
    
    optimized_prompt = optimize_prompt_text(name, age, genre, user_prompt)
    
    # Build character info string
    character_info = ""
    if name or age or gender:
        character_info = "Karakter Bilgileri:\n"
        if name:
            character_info += f"- İsim: {name}\n"
        if age:
            character_info += f"- Yaş: {age}\n"
        if gender:
            character_info += f"- Cinsiyet: {gender}\n"
        character_info += "\n"

    result = story_chain.invoke({
        "optimized_prompt": optimized_prompt,
        "character_info": character_info
    })
    return {
        "story": result.content.strip()
    } 