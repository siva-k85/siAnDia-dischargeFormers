"""
Chat assistant interface for the discharge summary generator.
Allows users to ask questions and get responses with conversation history.
"""

import streamlit as st
import sys
from pathlib import Path
import datetime
import json

# Add the parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import config
from llm.utils import setup_logging
from openai import OpenAI

st.set_page_config(page_title="Chat Assistant", page_icon="💬", layout="wide")

st.title("Medical Assistant Chat")
st.markdown(
    "Ask questions about discharge summaries, medical terminology, or how to use this application."
)

# Set up logging
logger = setup_logging(config.LOGS_DIR, config.LOG_LEVEL)


def get_assistant_response(messages, api_key, model):
    """Get a response from the LLM based on the conversation history."""
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": """You are a helpful medical assistant specializing in discharge summaries.
                    You can answer questions about medical terminology, best practices for discharge summaries,
                    and how to use this application. Keep responses focused on medical discharge summaries
                    and related healthcare topics. Be professional, accurate, and helpful.""",
                },
                *messages,
            ],
            temperature=0.3,
            max_tokens=1000,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error getting assistant response: {str(e)}")
        return f"Sorry, I encountered an error: {str(e)}"


def main():
    # Initialize chat history in session state if it doesn't exist
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Sidebar configuration
    with st.sidebar:
        st.header("Chat Settings")

        # API key input
        api_key = st.text_input(
            "OpenAI API Key", value=config.OPENAI_API_KEY, type="password"
        )

        # Model selection
        model = st.selectbox(
            "LLM Model", ["gpt-4", "gpt-4.5-preview", "gpt-3.5-turbo"], index=0
        )

        # Clear chat history
        if st.button("Clear Chat History"):
            st.session_state.chat_messages = []
            st.rerun()

        # Export chat history
        if st.session_state.chat_messages and st.button("Export Chat History"):
            # Convert messages to a text format
            chat_text = "\n".join(
                [
                    f"{msg['role'].upper()} ({msg.get('timestamp', 'unknown time')}): {msg['content']}"
                    for msg in st.session_state.chat_messages
                ]
            )

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            st.download_button(
                label="Download Chat Log",
                data=chat_text,
                file_name=f"chat_history_{timestamp}.txt",
                mime="text/plain",
            )

    # Display chat messages
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about discharge summaries..."):
        # Add user message to chat history
        user_message = {
            "role": "user",
            "content": prompt,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        st.session_state.chat_messages.append(user_message)

        # Display user message
        with st.chat_message("user"):
            st.write(prompt)

        # Prepare messages for API (without timestamps)
        api_messages = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in st.session_state.chat_messages
        ]

        # Get assistant response
        with st.spinner("Thinking..."):
            response_text = get_assistant_response(api_messages, api_key, model)

        # Add assistant message to chat history
        assistant_message = {
            "role": "assistant",
            "content": response_text,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        st.session_state.chat_messages.append(assistant_message)

        # Display assistant response
        with st.chat_message("assistant"):
            st.write(response_text)

        # Log the interaction
        logger.info(
            f"Chat interaction - User: {prompt[:50]}{'...' if len(prompt) > 50 else ''}"
        )


if __name__ == "__main__":
    main()
