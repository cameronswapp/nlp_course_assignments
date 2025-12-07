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
    system_prompt=("""You are AggieAI, an AI assistant to help Utah State fans with information about Aggie sports players."""
    ),
    tools = [tools.generateQuery, tools.databaseQuery, tools.ragTool],
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
