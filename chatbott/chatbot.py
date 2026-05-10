from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults
load_dotenv()
llm=ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    streaming=True
)
search_tool=TavilySearchResults(
    tavily_api_key=os.getenv('TAVILY_API_KEY'),
    max_results=3
)
prompt=ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
              You are a helpful ai assistant .
              Your responsibilty is:
                1. Answer the user's question to the best of your ability.
                2. If you don't know the answer, use the search tool to find the answer and provide it to the user.
                Always use the search tool if you don't know the answer to the user's question. Do not make up answers.
                Keep your answers concise and to the point. If you use the search tool, provide the answer in a clear and concise manner, and include the source of the information.
                Keep answers professional and beginner-friendly.
            """
            ),
            (
                "human",
                """
                User Question:{question}
                Internet Search Tool: {search_results}
                """
                
            )
    ]
)
parser=StrOutputParser()
chain=prompt |llm|parser 
def answer_question(question):
    search_results=search_tool.invoke(question)
    response_stream=chain.stream(
        {
            "question": question,
            "search_results": search_results
        }
    )
    return response_stream