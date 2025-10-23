import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.cache import SQLiteCache
from langchain.globals import set_llm_cache

# Load environment variables
load_dotenv()
set_llm_cache(SQLiteCache("cache/langchain_cache.db"))

def get_llm(model_name="openai/gpt-4.1-nano"):
    return ChatOpenAI(
        base_url=os.getenv("OPENROUTER_BASE"),
        model_name=model_name,
        api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=0.7,
    )

def get_response(llm, prompt):
    try:
        response = llm.invoke(prompt)
        print(f"Response: \n\n{response.content} \n")
        return response.content
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_response_with_system(llm, system_prompt, user_prompt):
    try:
        messages = [
            # Sets the context, role, and behavior of the AI 
            # When: Sent once at the beginning of the conversation
            # Content: Instructions about who the AI is and how it should behave
            {"role": "system", "content": system_prompt},
            # Purpose: Contains the actual question or task from the user
            # When: Sent each time the user asks something
            # Content: The specific question, request, or problem to solve
            {"role": "user", "content": user_prompt}
        ]
        response = llm.invoke(messages)
        print(f"Response: {response.content}")
        return response.content
    except Exception as e:
        print(f"Error: {e}")
        return None
