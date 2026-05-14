import streamlit as st
from research_graph import run_research_agent
st.set_page_config(
    page_title:"Agentic Research Assistant",
    layout="centered"
)
st.title("AI research Agent")
with st.sidebar:
    st.header("Project Flow")
    st.write("Planner Node")
    st.write("Research Node")
    st.write("Evaluator Node")
    st.write("Writer Node")
topic=st.text_input(
    "Enter your research topic:",
    placeholder= "Enter the topic you wants to research with this Research Agent",
)
if st.button("generate"):
    if not topic.strip():
        st.error("Please enter a Research topic")
    else:
        with st.spinner("Research is on the process"):
            result=run_research_agent(topic)
        st.success("Research Completed")
        st.balloons()
        st.subheader("Evaluator Output")
        st.write(result["evaluation"])
        st.subheader("Final research report")
        st.markdown(result["final_report"])
        