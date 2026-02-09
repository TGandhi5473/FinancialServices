from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import json

def create_vector_store(json_path, ticker):
    """Builds a local RAG index using Nomic embeddings."""
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # Bundle text sections for the embedding engine
    corpus = [
        f"SECTION: RISK FACTORS\n{data['risk_factors']}",
        f"SECTION: MANAGEMENT DISCUSSION\n{data['md_and_a']}",
        f"SECTION: LEGAL PROCEEDINGS\n{data['legal_proceedings']}"
    ]
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150)
    docs = splitter.create_documents(corpus)

    # Persist the database locally
    vector_db = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=f"vector_db/{ticker}"
    )
    return vector_db
