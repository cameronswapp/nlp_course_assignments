import chainlit as cl
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from langfuse import get_client
import sentence_transformers
import sqlite3
import os

import tools

# Load environment variables
load_dotenv()

# Create basic agent
agent = Agent(
    model='google-gla:gemini-2.5-flash-lite',
    deps_type = None,
    system_prompt=("""You are AggieAI, an AI assistant to help Utah State fans with information about Aggie sports players."""
    ),
    tools = [tools.databaseQuery, tools.ragTool],
    instrument = True
)

# @Agent.tool
# def databaseQuery(ctx: RunContext[None], query: str) -> list[dict]:
#     """
#     Use this function to execute a read-only SQL query against the Aggies database.
#     You should use this function any time a user asks for information about the Aggies sports players or their grades.
#     Generate the appropriate SQL query to get the information requested by the user.

#     param query: A read-only SQL query string.
#     """
#     uri = "file:aggies.db?mode=ro"
#     db_conn = sqlite3.connect(uri, uri=True)
#     db_conn.row_factory = sqlite3.Row  # makes rows behave like dicts
#     cursor = db_conn.cursor()

#     cursor.execute(query)
#     rows = cursor.fetchall()
#     db_conn.close()

#     # Convert sqlite Row objects > JSON-serializable dicts
#     return [dict(row) for row in rows]

# @Agent.tool
# def ragTool(query):
#     docs = []
#     docDir = "./rag_docs"
#     for filename in os.listdir(docDir):
#         if filename.endswith(".txt"):
#             with open(os.path.join(docDir, filename), "r") as f:
#                 filepath = os.path.join(docDir, filename)
#                 text = f.read()
#                 docs.append((filepath, text))

#     chunks = []
#     for filepath, text in docs:
#         # Simple chunking by splitting on newlines
#         for chunk in text.splitlines():
#             chunks.append(chunk)

#     # 1. Load embeddings
#     embeddings = []  # load from storage

#     # 2. Find top 10 embeddings based off query
#     model = sentence_transformers.SentenceTransformer('all-MiniLM-L6-v2')
#     query_embedding = model.encode(query)

#     similarities = model.similarity(query_embedding, embeddings)
#     top_10_embeddings = sorted(embeddings, key=lambda x: similarities[x], reverse=True)[:10]
    
#     # 3. Pass top 10 embeddings into ranker
#     reranker = sentence_transformers.SentenceTransformer('cross-encoder/ms-marco-MiniLM-L-6-v2')
#     ranked_chunks = reranker.rerank(query, top_10_embeddings)

#     # 4. Pass top 2 chunks to LLM
#     top_2_chunks = ranked_chunks[:2]
#     llm = agent.model
#     context1 = chunks[top_2_chunks[0]]
#     context2 = chunks[top_2_chunks[1]]
#     prompt = f"The user asked the following question: {query}\n\nHere are two relevant paragraphs to help give you context:\n{context1}\n{context2}"

#     # 5. Return result of LLM
#     response = llm.generate(prompt)
#     return response

@cl.on_chat_start
def start_chat():
    # Set message history for the user session when chat is started
    cl.user_session.set("message_history", [])


@cl.on_message
async def main(message: cl.Message):

    message_history = cl.user_session.get("message_history")

    # Initialize message object for streaming
    msg = cl.Message(content="")

    async with agent.run_stream(message.content, deps=Deps, message_history=message_history) as result:
        async for token in result.stream_text(delta=True, debounce_by=None):
            await msg.stream_token(token)

    message_history += result.all_messages()

    # This essentially sends the final message to the UI and moves on to next turn
    await msg.update()

langfuse = get_client()
Agent.instrument_all()
