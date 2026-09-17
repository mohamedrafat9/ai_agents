from langchain.agents import create_agent
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from src.llm.factory import get_llm

llm = get_llm(
    provider="groq",
    model="qwen/qwen3.8-27b",
)

db = SQLDatabase.from_uri("sqlite:///sqlagent/db/database.db")

toolkit = SQLDatabaseToolkit(
    db=db,
    llm=llm,
)

tools = toolkit.get_tools()

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=(
        "You are a SQL assistant. Use the database tools to answer questions. "
        "Always inspect the available tables before querying."
    ),
    debug=True,
)

response = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "How many customers are there in the database?",
        }
    ]
})

print(response["messages"][-1].content)