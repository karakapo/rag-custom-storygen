import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

from core.config import settings


# Initialize LLM for title generation
llm_for_title= ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=settings.GOOGLE_API_KEY,
    temperature=0.5
)

# Title generation prompt template (from user prompt)
title_prompt_template = ChatPromptTemplate.from_messages([
    ("system", """Sen yaratıcı ve etkileyici hikâye başlıkları üreten bir yapay zekâsın. Görevin, verilen kullanıcı promptuna (istemine) uygun, dikkat çekici ve özgün bir başlık üretmek. Başlık kısa, akılda kalıcı ve hikâyenin temasını yansıtmalı."""),
    ("human", """
    Kullanıcı promptu:
    {user_prompt}
    
    Lütfen bu prompta uygun yaratıcı ve etkileyici bir başlık öner:
    Sadece başlığı döndür.
    """)
])

title_chain = title_prompt_template | llm_for_title

def generate_title(user_prompt: str) -> str:
    """
    Generates a creative and catchy title for a story based on the user's prompt.
    Args:
        user_prompt (str): The original prompt from the user.
    Returns:
        str: The generated title.
    """
    result = title_chain.invoke({"user_prompt": user_prompt})
    return result.content.strip()
