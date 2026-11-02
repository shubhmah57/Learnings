import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import (
    Agent,
    ModelSettings,
    Runner,
    set_default_openai_client,
    set_tracing_disabled,
)


load_dotenv(override=True)

open_router_key = os.getenv('OPEN_ROUTER_API_KEY')
open_router_base_url = os.getenv('OPEN_ROUTER_BASE_URL')
openai = AsyncOpenAI(api_key=open_router_key, base_url=open_router_base_url)
set_default_openai_client(openai, use_for_tracing=False)
set_tracing_disabled(True)
instructions = """
You are a chat bot which responds to any question asked randomly.
"""
while True:
    question = input("You: ")

    if question.lower() == "exit":
        break
    model_settings = ModelSettings(max_tokens=200)
    agent = Agent(
        name="CMD CHAT BOT",
        instructions=instructions,
        model="gpt-4o-mini",
        model_settings=model_settings,
    )
    result = Runner.run_sync(agent, question)
    print(result.final_output)


