import streamlit as st
from rag import retrieve_chunks, generate_answer

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")

st.title("📚 Simple RAG Chatbot")

query = st.text_input("Ask your question:")

if query:

    with st.spinner("Searching..."):

        documents, metadata = retrieve_chunks(query)

        answer = generate_answer(query, documents)

    st.subheader("Answer")
    st.write(answer)

    st.subheader("Sources")

    if metadata:
        for item in metadata:
            if "source" in item:
                st.write(f"📄 {item['source']}")