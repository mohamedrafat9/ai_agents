from langchain.agents import create_agent
from src.llm.factory import get_llm
from yt.tools import tools ,get_full_metadata, fetch_transcript, search_youtube,get_thumbnails

llm=get_llm(provider="groq")

res=get_thumbnails.invoke("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
print(res)


agent =create_agent(
        model=llm,
        tools=tools,
        system_prompt="You are a helpful YouTube assistant.",
    )

        