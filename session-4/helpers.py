import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.cache import SQLiteCache
from langchain.globals import set_llm_cache

load_dotenv()
# cache_dir = os.path.join(os.path.dirname(__file__), "cache")
# os.makedirs(cache_dir, exist_ok=True)
# cache_path = os.path.join(cache_dir, "langchain_cache.db")
# set_llm_cache(SQLiteCache(cache_path))

def get_llm(model_name="openai/gpt-4o", temperature: float = 0.0):
    return ChatOpenAI(
        base_url=os.getenv("OPENROUTER_BASE"),
        model_name=model_name,
        api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=temperature,
    )
