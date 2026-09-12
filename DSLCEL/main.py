import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from DSLCEL.tools import *
from src.llm.factory import get_llm
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent

tools = [
    list_csv_files,
    preload_datasets,
    get_dataset_summaries,
    call_dataframe_method,
    evaluate_classification_dataset,
    evaluate_regression_dataset,
]

llm = get_llm(provider="groq")

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=(
        "You are a data science assistant. "
        "Use the available tools to analyze CSV files. "
        "First list the available CSV files. "
        "Then load and summarize the relevant dataset. "
        "Determine whether it is a classification or regression dataset. "
        "Ask the user for the target column if it is not obvious."
    ),
)

print("Ask questions about your datasets. Type 'exit' to quit.")

while True:
    try:
        user_input = input("You: ")
    except EOFError:
        break

    if user_input.strip().lower() in {"exit", "quit"}:
        break

    result = agent.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ]
        }
    )
    print(f"Agent: {result['messages'][-1].content}")

