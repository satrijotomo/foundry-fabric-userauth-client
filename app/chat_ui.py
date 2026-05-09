import sys
import os

# ✅ Fix import path for Streamlit
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import re

from app.config import (
    TENANT_ID,
    FOUNDRY_RESPONSES_URL,
    FOUNDRY_ACTIVITY_URL,
    validate_config,
)
from app.auth import UserAuth
from app.foundry_client import FoundryAgentClient


# -----------------------------
# Helpers
# -----------------------------

def extract_final_answer(response_json):
    for item in response_json.get("output", []):
        if (
            item.get("type") == "message"
            and item.get("role") == "assistant"
            and item.get("phase") == "final_answer"
        ):
            for content in item.get("content", []):
                if content.get("type") == "output_text":
                    return content.get("text")
    return "No response found."


def clean_text(text):
    return re.sub(r'【.*?】', '', text).strip()


# -----------------------------
# App Init
# -----------------------------

validate_config()

st.set_page_config(page_title="Foundry Chat", layout="centered")

st.title("💬 Foundry Agent Chat")

# -----------------------------
# Session State
# -----------------------------

if "auth" not in st.session_state:
    st.session_state.auth = UserAuth(TENANT_ID)


if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "client" not in st.session_state:
    st.session_state.client = FoundryAgentClient(
        auth_provider=st.session_state.auth,
        responses_url=FOUNDRY_RESPONSES_URL,
        activity_url=FOUNDRY_ACTIVITY_URL
    )


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:
    st.header("Session")

    st.write("Conversation ID:")
    st.code(st.session_state.conversation_id)

    if st.button("🆕 New Chat"):
        st.session_state.conversation_id = None
        st.session_state.chat_history = []
        st.success("New session started")


# -----------------------------
# Chat UI
# -----------------------------

for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)


prompt = st.chat_input("Ask your Fabric agent...")


if prompt:
    st.session_state.chat_history.append(("user", prompt))

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):

        response = st.session_state.client.call_responses(
            user_input=prompt,
            conversation_id=st.session_state.conversation_id
        )

        # ✅ Extract conversation_id FROM Foundry response
        conv = response.get("conversation")
        if conv and conv.get("id"):
            st.session_state.conversation_id = conv["id"]


        answer = extract_final_answer(response)
        answer = clean_text(answer)

    st.session_state.chat_history.append(("assistant", answer))

    with st.chat_message("assistant"):
        st.markdown(answer)