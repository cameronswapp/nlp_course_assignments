import sqlite3
import os
from dotenv import load_dotenv
from pydantic_ai import RunContext
import sentence_transformers
from sentence_transformers import util
from sentence_transformers.cross_encoder import CrossEncoder
from google import genai
import numpy as np
from exa_py import Exa

load_dotenv()

def databaseQuery(ctx: RunContext[str], query: str) -> list[dict]:
    """
    Use this function to execute a read-only SQL query against the Aggies database.
    You should use this function any time a user asks for information about the Aggies sports players or their grades.
    Generate the appropriate SQL query to get the information requested by the user.

    Here is the schema of the Aggies database:
    students table:
        - student_id (INTEGER, PRIMARY KEY)
        - name (TEXT)
        - grad_year (INTEGER)

    grades table:
        - grade_id (INTEGER, PRIMARY KEY)
        - student_id (INTEGER, FOREIGN KEY to students.student_id)
        - subject (TEXT)
        - grade (TEXT)

    sports table:
        - sport_id (INTEGER, PRIMARY KEY)
        - sport_name (TEXT)
    
    student_sports table:
        - student_id (INTEGER, FOREIGN KEY to students.student_id)
        - sport_id (INTEGER, FOREIGN KEY to sports.sport_id)
        - jersey_number (INTEGER)
        - championships_won (INTEGER)
        - position (TEXT)
        - years_played (INTEGER)


    If the user requests information about players or people, use the students table.
    The sports table only contains sport names and IDs.
    The student_sports table contains information about which students play which sports, their jersey numbers, positions, championships won, and years played.
    The grades table contains information about student grades in various subjects.

    Do not generate a query that does not adhere to the above schema.

    Use the result of the database query to answer the user's question.

    param query: A question about Aggie sports players or their grades.
    """
    uri = "file:aggies.db?mode=ro"
    db_conn = sqlite3.connect(uri, uri=True)
    db_conn.row_factory = sqlite3.Row
    cursor = db_conn.cursor()

    cursor.execute(query)
    rows = cursor.fetchall()
    db_conn.close()

    # Convert sqlite3.Row objects to plain dicts
    return [dict(row) for row in rows]

def ragTool(ctx: RunContext[str], query: str) -> dict:
    """
    Use this tool to answer questions about Aggie sports and gameday procedures via Retrieval Augmented Generation.
    This will be helpful when the user asks questions that are not related to specific players or their grades.
    This tool will search through a set of documents related to Aggie sports to find relevant information to answer the user's question.

    param query: A user question about Aggie sports or gameday procedures.

    Use the response from this tool to answer the user's question.
    """

    chunks = np.load("chunks.npy", allow_pickle=True)

    # 1. Load embeddings
    embeddings = np.load("embeddings.npy", allow_pickle=True)
    embeddings = np.array(embeddings.tolist(), dtype=np.float32)

    # 2. Find top 10 embeddings based off query
    model = sentence_transformers.SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode(query)

    similarities = util.cos_sim(query_embedding, embeddings)[0]
    top_indices = similarities.argsort(descending=True)[:10].cpu().numpy()
    
    # 3. Pass top 10 embeddings into ranker
    reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    candidate_chunks = [chunks[i] for i in top_indices]

    pairs = [(query, c) for c in candidate_chunks]

    # Cross-encoder scores
    scores = reranker.predict(pairs)  # shape: (num_chunks,)

    # Get indices of top 2 chunks (highest score = more relevant)
    top2_idx = np.argsort(scores)[::-1][:2]

    top_2_chunks = [candidate_chunks[i] for i in top2_idx]

    return {
        "query": query,
        "retrieved_chunks": top_2_chunks,
    }

exa = Exa(api_key=os.getenv("EXA_API_KEY"))

def websearch(ctx: RunContext[str], query: str) -> dict:
    """
    Search the web using Exa.ai.
    Use this tool when the user asks questions that require up-to-date information about Aggie sports, such as recent game results, player news, or upcoming events.
    If the user asks about the 'Aggies', make sure to search for the Utah State Aggies, as there are multiple schools whose nickname is the Aggies.

    param query: A user question that may require web search to answer.

    return: A dictionary containing the search results with titles, URLs, and snippets.

    Use the information from these results to answer the user's question.
    """
    results = exa.search_and_contents(
        query=query,
        type="auto",
        num_results=5,
    )

    # Convert Exa response into something the model can reason over
    items = []
    for r in results.results:
        items.append({
            "title": r.title,
            "url": r.url,
            "snippet": r.text or "",
        })

    return {"results": items}
