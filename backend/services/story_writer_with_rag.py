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
    ("system", """
You are an turkish AI storyteller.

The user will provide key story components. 
Your task is to craft a compelling, detailed, and immersive story based on these elements.

Guidelines:
- Follow the user's components closely and ensure the story has a clear structure: beginning, middle, and end.
- The setting should reflect the tone and genre.
- Incorporate all plot points logically and cohesively.
- Write in a vivid, descriptive, and emotionally engaging style.
- You may add creative twists or enriching elements, as long as the story remains coherent.

IMPORTANT: You must return a valid JSON object with exactly these keys:
{
  "title": "A creative title for the story",
  "content": "The full story text, richly written"
}

Do not include any other text or formatting outside this JSON structure.

Use these story components to guide the story creation:
{story_components}
    """)
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
    story_json = await asyncio.to_thread(
        lambda: story_writer_chain.invoke({"story_components": components})["story"]
    )
    
    try:
        # Parse the JSON response
        story = json.loads(story_json)
        # Validate required keys
        if "title" not in story or "content" not in story:
            raise ValueError("Story JSON must contain 'title' and 'content' keys")
        return story
    except json.JSONDecodeError as e:
        print("Failed to parse story JSON:", story_json)
        raise ValueError(f"Invalid JSON response from LLM: {str(e)}") 