import streamlit as st
from dotenv import load_dotenv
import os
import requests

load_dotenv()

st.set_page_config(page_title="LangGraph AI Agent ", page_icon="🤖", layout="centered",)
st.title("LangGraph AI Chatbot Agent")
st.write("Create and Write With AI Agent")

system_prompt = st.text_area("Define Your AI Agent: ", placeholder="Type your System prompt here...", height=70)

GROQ_MODEL_NAME = ["qwen/qwen3-32b","llama-3.3-70b-versatile","llama-3.1-8b-instant"]
OPEANAI_MODEL_NAME = []
# ["gpt-4o-mini"]
provider = st.radio("Select Provider",("Groq","OpenAI"))

if provider.lower() == "groq":
    selected_model = st.selectbox("Select Groq Model", GROQ_MODEL_NAME)
elif provider == "OpenAI":
    selected_model = st.selectbox("Select OpenAI Model", OPEANAI_MODEL_NAME)

allow_web_search = st.checkbox("Allow Web Search", value=False)

user_query = st.text_area("Your Query: ", placeholder="Ask Anythings", height=100)

#connect with backed url
API_URL = os.getenv("API_URL")
if st.button("Ask Agent"):
    if user_query.strip():
        payload = {
                "model_name": selected_model,
                "model_provider": provider,
                "system_prompt": system_prompt,
                "messages": [user_query],
                "allow_search": allow_web_search
            }
        response = requests.post(
            API_URL,
            json=payload
        )
        if response.status_code == 200:
            response_data = response.json()
            if "error" in response_data:
                st.error(f"Error: {response_data['error']}")
            else:
                st.subheader("AI Agent Response")
                st.markdown(f"**Final** **response:** {response_data}")

