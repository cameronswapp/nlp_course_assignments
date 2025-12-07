import sqlite3
import os
from dotenv import load_dotenv
from pydantic_ai import RunContext
import sentence_transformers
from sentence_transformers import util
from sentence_transformers.cross_encoder import CrossEncoder
from google import genai
import numpy as np

load_dotenv()

def generateQuery(ctx: RunContext[str], user_request: str) -> str:
    """
    Use this function to generate a read-only SQL query based on the user's request.

    The only tables you can use are: students, grades, sports, and student_sports.

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

    Do not generate a query that doesn't work with the schema provided.
    """
    llm = genai.Client()
    prompt = f"You are an expert SQL generator. The user asked for the information contained here: {user_request}. Based on the database schema provided, generate a read-only SQL query to retrieve the requested information. Do not generate a query that does not work with the schema provided. Only provide the SQL query without any additional text."
    response = llm.models.generate_content(
        model="gemini-2.5-flash",
        config=genai.types.GenerateContentConfig(
            system_instruction="The SQL query you generate must be read-only and work with the Aggies database schema provided."
        ),
        contents=prompt
    )
    return response.text

def databaseQuery(ctx: RunContext[str], query: str) -> str:
    """
    Use this function to execute a read-only SQL query against the Aggies database.
    You should use this function any time a user asks for information about the Aggies sports players or their grades.
    Use generateQuery to create the appropriate SQL query to get the information requested by the user.

    Use the result of the database query to answer the user's question.

    param query: A read-only SQL query string.
    """
    uri = "file:aggies.db?mode=ro"
    db_conn = sqlite3.connect(uri, uri=True)
    cursor = db_conn.cursor()

    cursor.execute(query)
    rows = cursor.fetchall()
    db_conn.close()

    # Convert sqlite Row objects → JSON-serializable dicts
    return rows

def ragTool(query):
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
    
    context1, context2 = top_2_chunks
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
