import pandas as pd
from semantic_kernel.functions import kernel_function
class CSVPlugin:
    @kernel_function(
        name="analyze_csv",
        description="Analyze a CSV file and return structured summary and text summary."
    )
    def analyze_csv(self, file_path: str) -> dict:
        df = pd.read_csv(file_path)
        rows, columns = df.shape
        column_names = list(df.columns)
        missing_values = df.isnull().sum().to_dict()
        data_types = df.dtypes.astype(str).to_dict()
        numeric_summary_df = df.describe().reset_index()
        sample_data_df = df.head(10)
        text_summary = f"""
CSV Analysis Result:

Total Rows: {rows}
Total Columns: {columns}

Column Names:
{column_names}

Data Types:
{data_types}

Missing Values:
{missing_values}

Numeric Summary:
{df.describe().to_string()}

Sample Data:
{df.head(5).to_string()}
"""

        return {
            "rows": rows,
            "columns": columns,
            "column_names": column_names,
            "missing_values": missing_values,
            "data_types": data_types,
            "numeric_summary": numeric_summary_df,
            "sample_data": sample_data_df,
            "text_summary": text_summary
        }