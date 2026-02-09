from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

def run_local_judge(ticker, query, mode="Local", api_key=None, high_precision=False):
    # 1. Setup Brain
    if mode == "OpenAI" and api_key:
        llm = ChatOpenAI(model="gpt-4o", api_key=api_key)
    else:
        llm = ChatOllama(model="deepseek-r1:7b")

    # 2. Retrieve Context
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma(persist_directory=f"vector_db/{ticker}", embedding_function=embeddings)
    docs = db.similarity_search(query, k=5)
    context = "\n---\n".join([d.page_content for d in docs])

    # 3. Primary Analysis Pass
    primary_prompt = f"Analyze {ticker} based on this context: {context}\nQuery: {query}"
    primary_verdict = llm.invoke(primary_prompt).content

    if not high_precision:
        return primary_verdict

    # 4. Evaluator Pass (The Audit)
    eval_prompt = f"""
    You are a Senior Financial Auditor. Critique this Analyst Report for {ticker}.
    
    REPORT TO AUDIT:
    {primary_verdict}
    
    SOURCE CONTEXT:
    {context}
    
    INSTRUCTIONS:
    1. Identify any facts in the report NOT found in the context (Hallucinations).
    2. Check if the numbers in the report match the context exactly.
    3. If errors are found, output 'REFINE' followed by the corrected report.
    4. If the report is perfect, output 'APPROVED' followed by the original report.
    """
    
    final_audit = llm.invoke(eval_prompt).content
    return final_audit
