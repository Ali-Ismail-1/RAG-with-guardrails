# ui/app.py
import streamlit as st
import requests

API_URL = "http://localhost:8000/chat"

st.set_page_config(page_title="Compliance-Safe RAG Chatbot", page_icon=":robot_face:")

st.title("Compliance-Safe RAG Chatbot")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input box
if prompt := st.chat_input("Ask me anything about the docs!"):
    # Add user message to chat history
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send to FastAPI Backend
    try:
        response = requests.post(
            API_URL, 
            json={"session_id": "demo", "question": prompt},
            timeout=30,
        )
        response.raise_for_status()
        answer = response.json().get("answer", "Sorry, I couldn't process your request.")
    except requests.exceptions.RequestException as e:
        answer = f"Sorry, I couldn't process your request. Error: {str(e)}"

    # Add assistant message to chat history
    st.session_state["messages"].append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)