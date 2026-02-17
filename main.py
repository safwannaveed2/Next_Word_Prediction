import streamlit as st
import requests

st.title("Next Word Prediction 📝")
http
user_input = st.text_input("Type something here:")

if st.button("Predict"):
    if user_input.strip() != "":
        try:
            response = requests.post(
               "https://huggingface.co/spaces/safwan-9/Next-word-prediction",
                json={"text": user_input}
            )
            if response.status_code == 200:
                st.success(f"Predicted next word: {response.json()['next_word']}")
            else:
                st.error(f"Error: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("FastAPI server is not running. Start it first!")
    else:
        st.warning("Please type some text first.")
