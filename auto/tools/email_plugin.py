from groq import Groq
from semantic_kernel.functions import kernel_funcion
from config import GROQ_API_KEY,GROQ_MODEL

class EmailPlugin:
    def __init__(self):
        self.client=Groq(api_key=GROQ_API_KEY)

    @kernel_function(
        name-"create_email_draft",
        description="Create a professional email draft from data summary and insights"
    )
    def create_emai_draft(self,insights:str)->str:
        prompt = f""" 
You are a professional assistant.

Create a clear and professional email draft based on these data insights:

{insights}

The email should include:
- Subject line
- Greeting
- Short summary
- Key insights
- Recommended action
- Polite closing
"""
        response=self.client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role":"system","content":"You wite professioal business email" },
                {"role":"user","content":prompt}
            ],
            temperature=0.4
        )
        return response.choices[0].message.content
