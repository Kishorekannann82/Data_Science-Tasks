import os
import pandas as pd
import streamlit as st
from agent import AutonomousTaskAgent
st.set_page_config(
    page_title="Autonomous CSV Insight Creator",
    layout="wide"
)
st.title("Autonomous CSV Insight and Email Generator")
st.write("Upload a CSV file. The agent will analyze it, generate insights, and create an email draft.")
agent = AutonomousTaskAgent()

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

task = st.text_area(
    "Enter your task",
    placeholder="Example: Analyze this CSV, summarize it, generate insights, and create an email draft for my senior."
)
if uploaded_file is not None:
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", uploaded_file.name)
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())
    st.success(f"File uploaded successfully: {uploaded_file.name}")
if st.button("Run Agent"):
    if uploaded_file is None:
        st.error("File not found. Upload a CSV first.")
    elif not task.strip():
        st.error("Please enter a task.")
    else:
        with st.spinner("Agent is analyzing the CSV and generating insights..."):
            result = agent.run(task=task, file_path=file_path)

        csv_result = result["csv_result"]
        st.divider()
        st.subheader("CSV Overview")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Rows", csv_result["rows"])
        with col2:
            st.metric("Total Columns", csv_result["columns"])
        with col3:
            st.metric("Columns With Missing Values", sum(1 for v in csv_result["missing_values"].values() if v > 0))

        st.divider()
        st.subheader("Column Names")
        st.dataframe(
            pd.DataFrame({"Columns": csv_result["column_names"]}),
            use_container_width=True
        )

        st.subheader("Data Types")
        st.dataframe(
            pd.DataFrame(
                list(csv_result["data_types"].items()),
                columns=["Column", "Data Type"]
            ),
            use_container_width=True
        )

        st.subheader("Missing Values")
        st.dataframe(
            pd.DataFrame(
                list(csv_result["missing_values"].items()),
                columns=["Column", "Missing Values"]
            ),
            use_container_width=True
        )

        st.subheader("Numeric Summary")
        st.dataframe(
            csv_result["numeric_summary"],
            use_container_width=True
        )

        st.subheader("Sample Data")
        st.dataframe(
            csv_result["sample_data"],
            use_container_width=True
        )

        st.divider()

        st.subheader("Generated Insights")
        st.markdown(result["insights"])

        st.divider()

        st.subheader("Email Draft")
        edited_email = st.text_area(
            "Review or edit the generated email",
            value=result["email_draft"],
            height=350
        )

        st.success(result["memory_status"])
        st.balloons()


with st.expander("View Recent Memory"):
    memory = agent.get_memory()
    st.code(memory)