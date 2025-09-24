import streamlit as st
from Langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

CONFIG = {"configurable": {"thread_id": "thread-1"}}

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

# Display previous conversation history
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])  # 👈 render as Markdown

# User input
user_input = st.chat_input("Type here")

if user_input:
    # Save user message
    st.session_state["message_history"].append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # Assistant streaming response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        # Stream response chunks
        for message_chunk, metadata in chatbot.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config=CONFIG,
            stream_mode="messages"
        ):
            if message_chunk.content:
                full_response += message_chunk.content
                placeholder.markdown(full_response + "▌")  # 👈 Markdown + typing cursor

        # Finalize response
        placeholder.markdown(full_response)

    # Save assistant reply
    st.session_state["message_history"].append(
        {"role": "assistant", "content": full_response}
    )
