import chromadb
import requests
import os

from dotenv import load_dotenv



# LOAD ENV VARIABLES


load_dotenv()

API_KEY = os.getenv("NVIDIA_API_KEY")



# CHROMADB SETUP


client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="rag_collection"
)



# RETRIEVE RELEVANT CHUNKS


def retrieve_chunks(query):

    results = collection.query(
        query_texts=[query],
        n_results=5
    )

    documents = results["documents"][0]

    metadata = results["metadatas"][0]

    return documents, metadata



# GENERATE ANSWER


def generate_answer(query, documents):

    context = "\n\n".join(documents)

    prompt = f"""
Answer the question using ONLY the context below.

Context:
{context}

Question:
{query}
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta/llama-3.1-70b-instruct",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2,
        "max_tokens": 512,
        "stream": False
    }

    response = requests.post(
        "https://integrate.api.nvidia.com/v1/chat/completions",
        headers=headers,
        json=payload
    )

    print("\nSTATUS CODE:", response.status_code)

    print("\nRAW RESPONSE:")
    print(response.text)

    
    if response.status_code != 200:
        return f"API Error: {response.text}"

    try:
        result = response.json()

        answer = result["choices"][0]["message"]["content"]

        return answer

    except Exception as e:

        return f"JSON Parsing Error: {str(e)}"



# MAIN RAG FUNCTION


def ask_rag(query):

    documents, metadata = retrieve_chunks(query)

    answer = generate_answer(query, documents)

    print("\nANSWER:\n")
    print(answer)

    print("\nSOURCES:\n")

    unique_sources = set()
    for item in metadata:
        unique_sources.add(item["source"])
    for source in unique_sources:
        print(f"- {source}")



# TERMINAL CHAT LOOP


while True:

    query = input("\nAsk a question (or type exit): ")

    if query.lower() == "exit":
        break

    ask_rag(query)