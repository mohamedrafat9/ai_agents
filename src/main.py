import os
import sys
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
# from langchain_core.output_parsers import JsonOutputParser
from langchain_openrouter import ChatOpenRouter

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from config import get_settings

settings = get_settings()

llm=ChatOpenRouter(
    model=settings.openrouter_model,
    api_key=settings.openrouter_api_key,
    temperature=0.7,
    max_tokens=1000
)

template = """
Analyze the following product review:
"{review}"

Provide your analysis in the following format:
- Sentiment: (positive, negative, or neutral)
- Key Features Mentioned: (list the product features mentioned)
- Summary: (one-sentence summary)
"""
prompt=PromptTemplate.from_template(template)

def format_review_prompt(var):
    return prompt.format(**var)

review_analysis_chain = (
    RunnableLambda(format_review_prompt)
    | llm
    | StrOutputParser()
)


reviews = [
    "I love this smartphone! The camera quality is exceptional and the battery lasts all day. The only downside is that it heats up a bit during gaming.",
    
    "This laptop is terrible. It's slow, crashes frequently, and the keyboard stopped working after just two months. Customer service was unhelpful."
]



for i, review in enumerate(reviews):

    print(f"==== Review #{i+1} ====")

    result = review_analysis_chain.invoke({
        "review": review
    })

    print(result)
    print()
