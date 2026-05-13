from groq import Groq
from semantic_kernel import kernel_function
from config import GROQ_API_KEY,GROQ_MODEL
class InsightPlugin:
    def __init__(self):
        self.client=Groq(api_key=GROQ_API_KEY)

    @kernel_function(
        name="generate_insights",
        description="Generate the useful business or data insights from a CSV analysis summary"
    )
    def generate_insights(self,csv_summary:str)->str:
        prompt=f""" 
You are a data analyst.
based on the following CSV analysis,generate clear and useful insights.
CSV Analysis:
{csv_summary}
Give the output in this format:
-Short Summary
-Key Insights
-Possible problem in data
-Recommenended actions
""" 
        response=self.client.chat.completions.create(
            model=GROQ_MODEL,
            message=[
                {"role":"system","content":"You are a helful data analyst."},
                {"role":"user","content":prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content