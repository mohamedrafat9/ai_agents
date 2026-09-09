from pyexpat import model
import re
from langchain_openrouter import ChatOpenRouter
#openai
from langchain_openai import ChatOpenAI
import sys
import os
from pathlib import Path
from config import get_settings
settings = get_settings()

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

llm = ChatOpenRouter(
    model=settings.openrouter_model,
    api_key=settings.openrouter_api_key,
    temperature=0.7,
    max_tokens=500
)
response = llm.invoke("What is tool calling in langchain?")
print("\nResponse Content: ", response.content)
