import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
load_dotenv()
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0
)
parser = JsonOutputParser()
prompt = ChatPromptTemplate.from_template(
    """
You are a Pizza Order AI Assistant.
Your task:
- Understand the user's pizza order.
- Extract the order details.
- Validate missing information.
- Return ONLY valid JSON.

Available pizzas:
- Chicken Pizza
- Veggie Pizza
- Paneer Pizza
- Cheese Pizza
- Chocolate Pizza

Available sizes:
- Small
- Medium
- Large

Valid intents:
- add_order
- ask_missing_info
- confirm_order
- cancel_order
- general_question

Required fields for adding pizza:
- pizza_name
- size
- quantity

Current order memory:
{order_memory}

User message:
{user_message}

Return JSON in this exact format:

{{
  "intent": "",
  "pizza_name": "",
  "size": "",
  "quantity": 0,
  "toppings": [],
  "missing_fields": [],
  "confirmation_message": ""
}}

Rules:
- If pizza_name, size, or quantity is missing, intent must be "ask_missing_info".
- If all required fields are present, intent must be "add_order".
- If user asks to confirm/finalize order, intent must be "confirm_order".
- If user wants to cancel order, intent must be "cancel_order".
- If user asks menu/general question, intent must be "general_question".
- If user says extra cheese, add "extra cheese" in toppings.
- If user says extra toppings, add "extra toppings" in toppings.
- Use null for missing pizza_name or size.
- Use 0 for missing quantity.
- Always write a clear confirmation_message.
- Return ONLY JSON.
"""
)

chain = prompt | llm | parser

def process_pizza_order(user_message, order_memory):

    response = chain.invoke(
        {
            "user_message": user_message,
            "order_memory": order_memory
        }
    )

    return response