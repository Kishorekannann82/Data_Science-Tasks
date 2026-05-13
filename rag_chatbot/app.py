import streamlit as st 
import os
from rag import ask_rag
st.set_page_config(
    page_title="Rag Chatbott",
    layout="centered"
)
st.title("Rag Chatbot")
st.write("Uploads PDF or CSV files")
uploaded_file=st.file_uploader("Upload PDF or CSV",type=["pdf","csv"])
question=st.text_input("Ask anything you want in the document")
ask_button=st.button("Ask Question")
if ask_button:
    if uploaded_file is None:
        st.warning("Please upload some document")
    elif not question:
        st.warning("Please ask a question")
    else:
        os.makedirs(
            "uploads",
            exist_ok=True
        )
        file_path=os.path.join(
            "uploads",
            uploaded_file.name
        )
        with open(file_path,"wb") as f:
            f.write(uploaded_file.getbuffer())
        with st.spinner("Processing yourrr documents"):
            response=ask_rag(file_path,question)
        st.subheader("Answer")
        st.write(response)