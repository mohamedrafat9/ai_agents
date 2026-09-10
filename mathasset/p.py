from langchain.agents import create_agent
from langchain.tools import tool
from src.llm.factory import get_llm


llm = get_llm()


@tool
def add_numbers(
    numbers: list[float],
    use_absolute: bool = False,
) -> float:
    """Add all numbers in the provided list."""

    if use_absolute:
        numbers = [abs(number) for number in numbers]

    return sum(numbers)


agent = create_agent(
    model=llm,
    tools=[add_numbers],
)


for state in agent.stream(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "In 2023, the US GDP was approximately $27.72 trillion, "
                    "Canada's was around $2.14 trillion, and Mexico's was "
                    "about $1.79 trillion. What is the total?"
                ),
            }
        ]
    },
    stream_mode="values",
):
    latest_message = state["messages"][-1]

    if latest_message.type == "tool":
        print("Tool result:", latest_message.content)

    elif latest_message.type == "ai" and latest_message.content:
        print("Assistant:", latest_message.content)