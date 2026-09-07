from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_openrouter import ChatOpenRouter
import os
import sys
from config import get_settings
settings = get_settings()
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)