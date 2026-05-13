import os
from typing import TypedDict,List
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from tavilly import TavillyClient
from langgraph.graph import StateGraph,END
load_dotenv()
llm=ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2,
    api_key=os.getenv("GROQ_API_KEY")
)
tavily_client=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
class ResearchState(TypedDict):
    topic:str
    questions:List[str]
    research_data:List[str]
    evaluation:str
    is_sufficient:bool
    final_report:str
def planner_node(state:ResearchState):
    """
    This node takes the user topic and breaks it into research questions. 
    """
    topic=state["topic"]
    prompt=f""" 
You are a research planner.
Topic:
{topic}
Break this topic into 5 clear research questions.
Rules:
-Return only the questions
-One question per line.
-Do not add numbering.
"""
    response=llm.invoke(prompt)
    questions=[
        q.strip
        for q in response.content.split("\n")
        if q.strip()
    ]
    return {
        "questions":questions
    }
def researcher_node(state:ResearchState):
    questions=state["questions"]
    research_data=[]
    for questions in questions:
        search_result=tavily_client.search(
            query=question,
            search_depth="basic",
            max_results=3
        )
        collected_text=f"\nQuestion:{question}\n"
        for result in search_result.get("results",[]):
            title=result.get("title","")
            content=result.get("content")
            url=result.get("url","")
            collected_text+=f""" 
Title:{title}
Content:{content}
Source:{url}
""" 
        research_data.append(collected_text)
    return {
        "research_data":research_data
    }