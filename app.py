import os
import streamlit as st
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

API_KEY = os.getenv("MISTRAL_API_KEY")  or st.secrets["MISTRAL_API_KEY"]
MODEL = "mistral-large-latest"

SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are Dr. Nova, a compassionate and experienced psychologist. "
        "You listen carefully, ask thoughtful open-ended questions, and help users "
        "explore their thoughts and feelings. You use evidence-based approaches such as "
        "CBT and motivational interviewing. You never diagnose or prescribe medication. "
        "If the user is in crisis or mentions self-harm, you gently encourage them to "
        "contact a professional or emergency services immediately. "
        "Always respond with empathy, patience, and without judgment."
        "anwer only in arabic "
    ),
}

st.set_page_config(page_title="Dr. Nova - Psychologist", page_icon="🧠", layout="centered")
st.title("🧠 Dr. Nova")
st.caption("Your compassionate AI psychologist — here to listen and support.")

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("Clear chat"):
    st.session_state.messages = []
    st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask me anything..."):
    if not API_KEY:
        st.error("MISTRAL_API_KEY not found in .env file.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    client = Mistral(api_key=API_KEY)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        stream = client.chat.stream(
            model=MODEL,
            messages=[SYSTEM_PROMPT] + st.session_state.messages,
        )

        for event in stream:
            delta = event.data.choices[0].delta.content
            if delta:
                full_response += delta
                placeholder.markdown(full_response + "▌")

        placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
