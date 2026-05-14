import os
from typing import TypedDict,List
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from tavily import TavilyClient
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
        q.strip()
        for q in response.content.split("\n")
        if q.strip()
    ]
    return {
        "questions":questions
    }
def researcher_node(state:ResearchState):
    questions=state["questions"]
    research_data=[]
    for question in questions:
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
def evaluator_node(state:ResearchState):
    topic=state["topic"]
    questions=state["questions"]
    research_data=state["research_data"]
    prompt=f""" 
You are a research quality evaluator.
Topic:
{topic}
Research Questions:
{questions}
Collected Research data:
{research_data}
Evaluate whether the research data is enough to write a good beginer friendly report.
Return your answer n this format:
Sufficient:YES or NO
Reason:
your reason here
""" 
    response=llm.invoke(prompt)
    evaluation_text=response.content
    is_sufficient="SUFFICIENT YES" in evaluation_text.upper()
    return {
        "evaluation":evaluation_text,
        "is_sufficient":is_sufficient
    }
def writer_node(state:ResearchState):
    topic=state["topic"]
    questions=state["questions"]
    research_data=state["research_data"]
    evaluation=state["evaluation"]
    prompt=f""" 
You are professional research report writer.
Write a clear,begineer friendly research report.
Topic:
{topic}
Research Questions:
{questions}

Research Data:
{research_data}

Evaluator Feedback:
{evaluation}

Report format:

# Title

## Introduction

## Research Questions

## Key Findings

## Detailed Explanation

## Benefits

## Challenges

## Real-World Examples

## Conclusion
## Sources
# Rules:
- Use simple English.
- Make it easy for beginners.
- Include source URLs in the Sources section.
- Do not make unsupported claims.
"""
    response=llm.invoke(prompt)
    return{
        "final_report":response.content
    }
def route_after_evaluation(state:ResearchState):
    if state["is_sufficient"]:
        return "writer"
    else:
        return "writer"
#workflow
workflow=StateGraph(ResearchState)
workflow.add_node("planner",planner_node)
workflow.add_node("researcher",researcher_node)
workflow.add_node("evaluator",evaluator_node)
workflow.add_node("writer",writer_node)
workflow.set_entry_point("planner")
workflow.add_edge("planner","researcher")
workflow.add_edge("researcher","evaluator")
workflow.add_conditional_edges(
    "evaluator",
    route_after_evaluation,
    {
        "writer":"writer"
    }
)
workflow.add_edge("writer",END)
research_app=workflow.compile()
def run_research_agent(topic:str):
    initial_state={
        "topic":topic,
        "questions":[],
        "research_data":[],
        "evaluation":"",
        "is_sufficient":False,
        "final_report":""
    }
    result=research_app.invoke(initial_state)
    return result 