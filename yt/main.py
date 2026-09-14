from langchain.agents import create_agent
from src.llm.factory import get_llm
from yt.tools import tools ,get_full_metadata, fetch_transcript, search_youtube,get_thumbnails,fix_arabic
from langchain_core.messages import HumanMessage
from langchain_core.messages import ToolMessage 
llm=get_llm(provider="groq")



agent =create_agent(
        model=llm,
        tools=tools,
        system_prompt=(
        "You are a helpful YouTube assistant. "
        "To summarize a video, extract its video ID, fetch the transcript, "
        "and summarize it in the requested language. "
        "For long transcripts, use only a reasonable amount of text."
    ),
    )

prompt = "I want to summarize youtube video: https://www.youtube.com/watch?v=ZWdF4gHC214 in arabic"
res=agent.invoke(
    {
        "messages":[
            {
                "role":"user",
                "content":prompt,
            }
        ]
    }
)

ans=res["messages"][-1].content
print(fix_arabic(ans))