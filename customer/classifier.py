import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
llm=ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0
)
parser=StrOutputParser()
prompt=ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a customer support ticket classifier.
            Your task is to classify into one of these categories:
            -Billing
            -Technical
            -Complaint
            -Feedback
            Return Only valid json format.
            {{
                "category":"Billing" 
            }}
            """
        ),
        (
            "human",
            """
            example:
            Ticket:
            "I was charged twice for my subscription"
            Output:
            {{
                "category" : "Billing" 
            }}
            Ticket:
            "The app crashes when i upload a file" 
            Output: 
            {{
                "category":"Technical" 
            }}
            Ticket:
            Your support team is very very rude
            Output:
            {{
                "category":"Complaint" 
            }}
            Ticket:
            "I really love the kindness of the Data Science Team during the onboard of new interns." 
            Output:
            {{
                "category":"Feedback" 
            }}
            Now classify this ticket:
            Ticket:
            {ticket}
            """
            
        )
    ]
)
chain=prompt|llm|parser 
def classify(ticket):
    response=chain.invoke({
        "ticket":ticket
    })
    return response
