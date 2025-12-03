import sqlite3
import os
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
import sentence_transformers
from google import genai

load_dotenv()

@Agent.tool
def databaseQuery(ctx: RunContext[None], query: str) -> list[dict]:
    """
    Use this function to execute a read-only SQL query against the Aggies database.
    You should use this function any time a user asks for information about the Aggies sports players or their grades.
    Generate the appropriate SQL query to get the information requested by the user, and pass this to the function as 'query'.

    param query: A read-only SQL query string.
    """
    uri = "file:aggies.db?mode=ro"
    db_conn = sqlite3.connect(uri, uri=True)
    db_conn.row_factory = sqlite3.Row  # makes rows behave like dicts
    cursor = db_conn.cursor()

    cursor.execute(query)
    rows = cursor.fetchall()
    db_conn.close()

    # Convert sqlite Row objects → JSON-serializable dicts
    return [dict(row) for row in rows]

@Agent.tool
def ragTool(query):
    docs = []
    docDir = "./rag_docs"
    for filename in os.listdir(docDir):
        if filename.endswith(".txt"):
            with open(os.path.join(docDir, filename), "r") as f:
                filepath = os.path.join(docDir, filename)
                text = f.read()
                docs.append((filepath, text))

    chunks = []
    for filepath, text in docs:
        # Simple chunking by splitting on newlines
        for chunk in text.splitlines():
            chunks.append(chunk)

    # 1. Load embeddings
    embeddings = []  # load from storage

    # 2. Find top 10 embeddings based off query
    model = sentence_transformers.SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode(query)

    similarities = model.similarity(query_embedding, embeddings)
    top_indices = similarities.argsort()[::-1][:10]
    top_10_embeddings = [embeddings[i] for i in top_indices]
    
    # 3. Pass top 10 embeddings into ranker
    reranker = sentence_transformers.SentenceTransformer('cross-encoder/ms-marco-MiniLM-L-6-v2')
    ranked_chunks = reranker.rerank(query, top_10_embeddings)

    # 4. Pass top 2 chunks to LLM
    top_2_chunks = ranked_chunks[:2]
    
    context1 = chunks[top_2_chunks[0]]
    context2 = chunks[top_2_chunks[1]]
    prompt = f"The user asked the following question: {query}\n\nHere are two relevant paragraphs to help give you context:\n{context1}\n{context2}"

    llm = genai.Client()
    response = llm.models.generate_content(
        model="gemini-2.5-flash",
        config=genai.types.GenerateContentConfig(
            system_instruction="You are an Aggie assistant that helps retrieve information from Aggie sports documents"
        ),
        contents=prompt
    )
    # 5. Return result of LLM
    return response.text
