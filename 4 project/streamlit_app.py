import streamlit as st
from rag_pipeline import ask

st.set_page_config(page_title="RAG Assistant", layout="wide")

st.title("📚 RAG Assistant")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Input box
query = st.chat_input("Ask something...")

if query:
    # Show user message
    st.chat_message("user").write(query)
    st.session_state.messages.append({"role": "user", "content": query})

    # Get response
    result = ask(query)
    answer = result["answer"]

    # Show bot response
    st.chat_message("assistant").write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})

    # Show sources (optional)
    if "Not found" not in answer:
        with st.expander("📚 Sources"):
            for src in result["sources"]:
                st.write(f"File: {src['file']} | Chunk: {src['chunk']}")