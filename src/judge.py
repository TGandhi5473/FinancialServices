from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

def run_local_judge(ticker, query, mode="Local", api_key=None):
    """The Agentic Brain: Reasons using the selected LLM."""
    if mode == "OpenAI" and api_key:
        llm = ChatOpenAI(model="gpt-4o", api_key=api_key)
    else:
        # DeepSeek-R1 is excellent for local financial reasoning
        llm = ChatOllama(model="deepseek-r1:7b")

    # Load context from Vector DB
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma(persist_directory=f"vector_db/{ticker}", embedding_function=embeddings)
    
    # Retrieve top 5 most relevant segments
    context_docs = db.similarity_search(query, k=5)
    context_text = "\n---\n".join([d.page_content for d in context_docs])

    system_prompt = f"""
    You are an AI Financial Auditor. Analyze the provided SEC 10-K context for {ticker}.
    Answer the user query with professional rigor. 
    If you see contradictory environmental or solvency risks, highlight them.
    
    CONTEXT:
    {context_text}
    """
    
    # Simple chain-of-thought style invocation
    response = llm.invoke([("system", system_prompt), ("human", query)])
    return response.content
