# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import ChatPromptTemplate
# from langchain.chains import LLMChain
# from typing import Dict, Any
# import os 
# from dotenv import load_dotenv
# import asyncio
# import json
# import logging
# from pydantic import BaseModel, Field

# load_dotenv()

# # Initialize LLM for component extraction
# llm_for_components = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash",
#     google_api_key=os.getenv("GOOGLE_API_KEY"),
#     temperature=0.7,
#     convert_system_message_to_human=True
# )

# component_extraction_prompt = ChatPromptTemplate.from_messages([
#     ("system", """You are a story component analyzer. Your task is to extract key components from a story prompt.
#     You MUST respond in valid JSON format with exactly these fields:
#     {
#         "main_character": "Description of main character",
#         "environment": "Description of environment",
#         "main_conflict": "Description of main conflict",
#         "moral": "Moral of the story",
#         "plot": "Main plot points",
#         "character_goal": "Character's main goal",
#         "genre": "Story genre",
#         "final_type": "Type of ending"
#     }

#     Rules:
#     1. All values must be in Turkish
#     2. If you can't determine a component, use an empty string
#     3. Do not include any text outside the JSON structure
#     4. Make sure the JSON is properly formatted
#     """),
#     ("human", """
#     Extract story components from this prompt:
#     {prompt}
#     """)
# ])

# component_extraction_chain = LLMChain(
#     llm=llm_for_components,
#     prompt=component_extraction_prompt,
#     output_key="components"
# )

# logger = logging.getLogger(__name__)

# class StoryComponentModel(BaseModel):
#     main_character: str = Field(default="", description="Description of main character")
#     environment: str = Field(default="", description="Description of environment")
#     main_conflict: str = Field(default="", description="Description of main conflict")
#     moral: str = Field(default="", description="Moral of the story")
#     plot: str = Field(default="", description="Main plot points")
#     character_goal: str = Field(default="", description="Character's main goal")
#     genre: str = Field(default="", description="Story genre")
#     final_type: str = Field(default="", description="Type of ending")

#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "main_character": "Küçük bir çocuk",
#                 "environment": "Orman",
#                 "main_conflict": "Kaybolma",
#                 "moral": "Cesaret ve azim",
#                 "plot": "Çocuk ormanda kaybolur ve eve dönmeye çalışır",
#                 "character_goal": "Eve dönmek",
#                 "genre": "Macera",
#                 "final_type": "Mutlu son"
#             }
#         }

# async def story_components(prompt: str) -> StoryComponentModel:
#     """
#     Extract story components from a prompt.
    
#     Args:
#         prompt (str): The story prompt to analyze
        
#     Returns:
#         StoryComponentModel: A Pydantic model containing all story components
#     """
#     # Run the chain and get the result
#     result = await asyncio.to_thread(
#         lambda: component_extraction_chain.invoke({"prompt": prompt})
#     )
#     result_str = result["components"]
    
#     # Try to parse the result as JSON
#     try:
#         # First try direct JSON parsing
#         result_dict = json.loads(result_str)
#     except json.JSONDecodeError:
#         # If that fails, try to extract JSON from the string
#         import re
#         json_match = re.search(r'\{[\s\S]*\}', result_str)
#         if json_match:
#             try:
#                 result_dict = json.loads(json_match.group())
#             except json.JSONDecodeError:
#                 result_dict = {}
#         else:
#             result_dict = {}
    
#     # Create Pydantic model from the result
#     try:
#         components = StoryComponentModel(**result_dict)
#         return components
#     except Exception:
#         return StoryComponentModel()

