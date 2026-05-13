import pandas as pd
from semantic_kernel.functions import kernel_function
class CSVPlugin:
    @kernel_function(name="analyze_csv",description="Analyze a CSV file and return rows and columns missing valus ,data types")
    def analyze_csv(self,file_path:str)->str:
        df=pd.read_csv(file_path)
        rows,columns=df.shape
        missing_values=df.isnull().sum().to_dict()
        data_types=df.dtypes.astype(str).to_dict()
        numeric_summary=df.describe().to_string()
        sample_data=df.head(5).to_string()

        result=f""" 
CSV Analysis Result:
Total Rows :{rows}
Total Columns:{columns}
Column Names:{list(df.columns)}
Data Types:{data_types}
Numeric Summary:{numeric_summary}
Sample Data:{sample_data}
""" 
        return result 