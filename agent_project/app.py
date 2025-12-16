import chainlit as cl
from dotenv import load_dotenv
from pydantic_ai import Agent
from langfuse import get_client

import tools

# Load environment variables
load_dotenv()

# Create basic agent
agent = Agent(
    model='google-gla:gemini-2.5-flash-lite',
    deps_type = str,
    system_prompt=("""You are AggieAI, an AI assistant to help Utah State fans with information about Aggie sports players.
                   If the user asks a question that is related to players, grades, classes, or sports, you must use the generateQuery and databaseQuery tools to get the information from the database.
                   Only generate SQL queries that are read-only and work with the provided database schema.
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
                   
                   If the user asks questions about other topics, first use the ragTool to get relevant information from the provided documents, then use that information to answer the user's question.
                   If the user asks questions that are very recent or about current events, use the websearch tool to get the latest information from the web to answer the user's question.
                   """
    ),
    tools = [tools.databaseQuery, tools.ragTool, tools.websearch],
    instrument = True
)

@cl.on_chat_start
def start_chat():
    # Set message history for the user session when chat is started
    cl.user_session.set("message_history", [])


@cl.on_message
async def main(message: cl.Message):

    message_history = cl.user_session.get("message_history")

    # Initialize message object for streaming
    msg = cl.Message(content="")

    async with agent.run_stream(message.content, message_history=message_history) as result:
        async for token in result.stream_text(delta=True, debounce_by=None):
            await msg.stream_token(token)

    message_history += result.all_messages()

    # This essentially sends the final message to the UI and moves on to next turn
    await msg.update()

langfuse = get_client()
Agent.instrument_all()
