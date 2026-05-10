from email_generator import generate_email
import streamlit as st
st.set_page_config(
    page_title="AI Email Generator",
    layout="centered"
)
st.title("AI Email Generator")
st.write("Generate professional emails with ease.")
purpose=st.text_input("Enter email Purpose")
tone=st.selectbox(
    "Select Tone",
    [
        "Professional",
        "Friendly",
        "Formal",
        "Apologetic",
        "Confident"
    ]
)
audience=st.text_input("Who is the audience for this email?")
details=st.text_area("Additional Details (Optional)")
generate_button=st.button(
    "Generate Email"
)
if generate_button:
    if not purpose:
        st.warning("Please enter a purpose for the email.")
    else:
        st.subheader("Generated Email")
        response_placeholder=st.empty()
        full_response=""
        response_stream=generate_email(purpose,tone,audience,details)
        for chunk in response_stream:
            full_response+=chunk
            response_placeholder.markdown(
                full_response
            )

            