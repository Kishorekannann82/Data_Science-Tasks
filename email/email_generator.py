import os 
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
llm=ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    streaming=True
)
prompt=ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
                You are a professional email writing assistant.
                Generate clear and professional emails.
                Always include
                -Subject Line
                -Greeting
                -Body
                -Closing

            """
            
        ),
        (
            "human",
            """
                Purpose :{purpose}
                Tone:{tone}
                Audience:{audience}
                Additional Detaiuls:
                {details}
            """
        )
    ]
)
parser=StrOutputParser()
chain=prompt|llm|parser
def generate_email(purpose,tone,audience,details):
    response=chain.stream(
        {
            "purpose":purpose,
            "tone":tone,
            "audience":audience,
            "details":details
        }
    )
    return response