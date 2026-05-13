import json
import os
from datetime import datetime
from semantic_kernel.functions import kernel_function 
class MemoryPlugin:
    def __init__(self,memory_file:str="memory/memory.json"):
        self.memory_file=memory_file
        os.makedirs(os.path.dirname(self.memory_file),exist_ok=True)
        if not os.path.exists(self.memory_file):
            with open(self.memory_file,"w") as file:
                json.dump([],file)
        @kernel_function(
            name="save_memory",
            description="Save tasks,summary,insights and email draft into the memory"
        )
        def save_memory(self,task:str,csv_summary:str,insights:str,email_draft:str)->str:
            with open(self.memory,"r") as file:
                memory_data=json.load(file)
            new_record={
                "time_stamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "task":task,
                "csv_summary":csv_summary,
                "insights":insights,
                "email_draft":email_draft
            }
            memory_data.append(new_record)
            with open(self.memory_file,"w") as file:
                json.dump(memory_data,file,indent=4)
            return "Memory Saved Sucessfully"
        @kernel_function(
            name="load_memory",
            description:"Load previous task memory"
        )
        def load_memory(self)->str:
            with open(self.memory_file,"r") as f:
                memory_data=json.load(file)
            if not memory_data:
                return "No Memory found"
            return json.dumps(memory_data[-3:],indent=4)