import streamlit as st
from classifier import classify
st.set_page_config(
    page_title="GeakMinds Customer support Ticket Classifier",
    layout="centered"
)
st.title("GeakMinds Customer Support Ticker Classifier")
st.write(
    "Classify your tickets using Ai"
)
ticket=st.text_area("Tell something",height=200)
classify_button=st.button("Classify Ticket")
if classify_button:
    if not ticket:
        st.warnings("Please enter something")
    else:
        with st.spinner(
            "Classifying on the process"
        ):
            response=classify(ticket)
            st.subheader("Classification Category Result")
            st.code(
                response,
                language="json"
            )
