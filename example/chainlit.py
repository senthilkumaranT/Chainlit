import os
import chainlit as cl
import asyncio
from retrieve import *
from openai import AsyncClient

# Initialize OpenAI client with base URL and API key
openai_client = AsyncClient(base_url="", api_key="")

# Configuration settings for OpenAI API
settings = {
    "temperature": 0.3,
    "max_tokens": 500,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}

@cl.on_chat_start
async def start_chat():
    # Set initial message history for the user session
    cl.user_session.set(
        "message_history",
        [
            {
                "role": "system",
                "content": "you are a helpful assistant",
            }
        ],
    )

async def answer_as(name):
    # Retrieve message history from user session
    message_history = cl.user_session.get("message_history")
    msg = cl.Message(author=name, content="")
    
    # Get data chunk based on user message
    datachunk = retrieve(msg.content, "docling")
    
    # Create a chat completion request to OpenAI
    stream = await openai_client.chat.completions.create( 
        model="deepseek/deepseek-r1-distill-llama-70b",
        messages=message_history + [{"role": "user", "content": f"""
        content : {datachunk}
        
        Question :{msg.content}
        
        based on user question and context give the answer                              
        """}],
        stream=True,
        **settings,
    )
    print(stream)
    # Stream the response tokens back to the user
    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await msg.stream_token(token)

    # Append the assistant's response to the message history
    message_history.append({"role": "assistant", "content": msg.content})
    await msg.send()

@cl.on_message
async def main(message: cl.Message):
    # Append the user's message to the message history
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    # Process the user's message and generate a response
    await asyncio.gather(answer_as("sk"))