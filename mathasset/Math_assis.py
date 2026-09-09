from langchain_openrouter import ChatOpenRouter
#messeges
from langchain_core.messages import HumanMessage, ToolMessage
# from langchain.agents import Tool
from langchain.tools import tool
import sys
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
@tool # generate a structured schema for the tool then the llm fills the schema with the required arguments and invokes the tool
def add_numbers(numbers: list[float],abs:bool=False) -> float:
    """Add all numbers in the provided list."""
    if abs:
        numbers = [abs(n) for n in numbers]
    return sum(numbers)

tools={
    "add_numbers": add_numbers
}

llm_with_tools=llm.bind_tools(list(tools.values()))

messages=[
    HumanMessage(
        content="Use the add_numbers tool to add [-1.1, -2.1, -3.0]. "
    )
]
response = llm_with_tools.invoke(messages)
print("\nResponse Content: ", response.content)
print("\nTool Calls: ", response.tool_calls)

for tool_call in response.tool_calls:
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    result = tools[tool_name].invoke(tool_args)

    print("Tool Result:", result)