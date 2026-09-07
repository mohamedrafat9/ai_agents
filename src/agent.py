import sys
from pathlib import Path

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openrouter import ChatOpenRouter

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import get_settings


settings = get_settings()


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


@tool
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


llm = ChatOpenRouter(
    model=settings.openrouter_model,
    api_key=settings.openrouter_api_key,
    temperature=0.6,
    max_tokens=1000,
)

tools = {
    "multiply": multiply,
    "add": add,
}

llm_with_tools = llm.bind_tools(list(tools.values()))

messages = [
    HumanMessage(
        content="What is 7 multiplied by 8, then add 5?"
    )
]

while True:
    response = llm_with_tools.invoke(messages)
    messages.append(response)

    if not response.tool_calls:
        print(response.content)
        break

    for tool_call in response.tool_calls:
        selected_tool = tools[tool_call["name"]]
        result = selected_tool.invoke(tool_call["args"])

        messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"],
            )
        )