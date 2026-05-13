import os
import streamlit as st 
from agent import AutonomousTaskAgent
st.set_page_config(
    title="Autonomous CSV Insight Creator",
    layout="centered"
)
st.title("Autonomous CSV Insight and Email Generator")
st.write("Upload a CSV and agent analyse it and create te insights and sed a email draft")
agent=AutonomousTaskAgent()
uploaded_file=st.file_uploader("Upload a csv file",type=["csv"])
task=st.text_area(
    "Enter your task",
    placeholder="Example:Analyze the Csv and create a insight and create a email draft"
)
if uploaded_file is not None:
    os.makedirs("uploads",exist_ok=True)
    file_path=os.path.join("uploads",uploaded_file.name)
    with open(file_path,"wb") as file:
        file.write(uploaded_file.get_buffer())
    st.success(f"File uploaded Successfully:{uploaded_file.name}")
if st.button("RUn Agent"):
    if uploaded_file is None:
        st.error("FIle not Found!Upload a csv and thena analyse")
    elif not task.strip():
        st.error("Please enter a task")
    else:
        with st.spinner("Agent is on the way...."):
            result=agent.run(task=task,file_path=file_path)
            st.subheader("CSV Summary")
            st.text(result["csv_summary"])
            st.subheader("Generated Insights")
            st.markdown(result["insights"])

            st.subheader("Email Draft")
            st.text_area("Generated Email", value=result["email_draft"], height=300)

            st.success(result["memory_status"])
            st.balloons()
with st.expander("View recent Memory"):
    memory=agent.get_memory()
    st.code(memory)
    