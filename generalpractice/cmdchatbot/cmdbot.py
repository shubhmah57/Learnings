import os
from dotenv import load_dotenv
from openai import OpenAI
from agents import Agent, Runner, trace, set_default_openai_client, set_tracing_disabled


load_dotenv(override=True)

open_router_key = os.getenv('OPEN_ROUTER_API_KEY')
open_router_base_url = os.getenv('OPEN_ROUTER_BASE_URL')
openai = OpenAI(api_key=open_router_key, base_url=open_router_base_url)
instructions = """
You are a chat bot which responds to any question asked randomly.
"""
while True:
    question = input("You: ")

    if question.lower() == "exit":
        break

    agent = Agent(name="Pandit Ji", instructions=instructions, model="gpt-4o-mini")   
    result = Runner.run(agent, question)
    print(result.final_output)




