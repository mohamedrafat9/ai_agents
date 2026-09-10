from src.llm.factory import get_llm


llm = get_llm()

print("LLM type:", type(llm).__name__)
print("LLM model:", llm.model)