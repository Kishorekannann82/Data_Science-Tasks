import streamlit as st
from chatbot import answer_question

st.set_page_config(
    page_title="Kishore AI Chatbot",
    layout="centered"
)
st.title("Kishore AI Assistant")
if "messages" not in st.session_state:
    st.session_state.messages=[]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    
user_input=st.chat_input("Ask me anyththing you want")
if user_input:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        response_paceholder=st.empty()
        full_response=""
        response=answer_question(user_input)
        for chunk in response:
            full_response+=chunk
            response_paceholder.markdown(full_response)
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )