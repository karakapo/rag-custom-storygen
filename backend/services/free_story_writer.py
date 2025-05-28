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
    ("system", """You are a creative story writer that focuses on originality and emotional depth.
    Your task is to write a story that:
    1. Is completely original and creative
    2. Has deep character development
    3. Contains unexpected plot twists
    4. Evokes strong emotions
    5. Is memorable and engaging"""),
    ("human", """
    Write a creative and original story based on this optimized prompt:
    
    {optimized_prompt}
    
    Guidelines:
    1. Be creative and original
    2. Don't follow any specific template
    3. Focus on character development and emotional depth
    4. Create unexpected plot twists
    5. Make the story engaging and memorable
    
    Return only the story, no additional text.
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