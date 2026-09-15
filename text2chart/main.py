import pandas as pd
from langchain_experimental.agents.agent_toolkits import (
    create_pandas_dataframe_agent,
)
from src.llm.factory import get_llm

df=pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/ZNoKMJ9rssJn-QbJ49kOzA/student-mat.csv"
)

llm=get_llm(
    provider="groq",
     model="qwen/qwen3.8-27b",

    )

agent = create_pandas_dataframe_agent(
    llm=llm,
    df=df,
    verbose=True,
    return_intermediate_steps=True,
    allow_dangerous_code=True,
    prefix=(
        "You are a pandas data analysis agent. "
        "Use pandas to analyze the dataframe. "
        "Use matplotlib when the user requests a chart. "
        "and explain the result briefly."
    ),
)

result = agent.invoke(
    {
        "input": (
            "Create box plots to analyze the relationship between 'freetime' (amount of free time) and 'G3' (final grade) across different levels of free time."
            "by gender and save it as text2chart/chart3.png."
        )
    }
)

print(result["output"])
