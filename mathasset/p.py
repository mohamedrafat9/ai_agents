from langchain.agents import create_agent
from langchain.tools import tool
from mathasset.tools import divide_numbers, multiply_numbers, subtract_numbers, add_numbers
from src.llm.factory import get_llm

llm = get_llm(provider="groq")

agent = create_agent(
    model=llm,
    tools=[add_numbers, subtract_numbers, multiply_numbers, divide_numbers],
    system_prompt="You are a helpful assistant that can perform basic arithmetic operations. You have access to the following tools: add_numbers, subtract_numbers, multiply_numbers, divide_numbers. Use these tools to answer user queries.",
)

user_input="divide_numbers([10, 2])"
for state in agent.stream(
    {
        "messages": [
            {
                "role": "user",
                "content": user_input
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