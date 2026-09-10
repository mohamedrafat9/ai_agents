from src.llm.factory import get_llm


llm = get_llm(provider="openai")

response = llm.invoke(
    "Reply with exactly: The provider connection works."
)

print(response.content)