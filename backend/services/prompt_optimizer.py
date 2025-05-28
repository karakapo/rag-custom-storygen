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
    temperature=0.3,
    convert_system_message_to_human=True
)



def optimize_prompt_text(name: str, age: int, genre: str, preferences: str) -> str:
    
    optimization_template = ChatPromptTemplate.from_messages([
    ("system", """You are an expert prompt optimizer for AI systems. Your task is to enhance user prompts by:
    1. Correcting spelling and grammar errors
    2. Making the prompt more detailed and specific
    3. Optimizing it for better AI understanding
    4. Maintaining the original intent while improving clarity
    5. Adding necessary context if missing
    
    Focus on making the prompt:
    - Clear and unambiguous
    - Well-structured
    - Specific and detailed
    - Free of errors
    - Optimized for AI comprehension"""),
    ("human", """
    Please optimize this prompt for better AI understanding:
    Character Name: {name}
    Character Age: {age}
    Genre: {genre}
    Preferences: {preferences}
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
        "preferences": preferences
    })
    return result