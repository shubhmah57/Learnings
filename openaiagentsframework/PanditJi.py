import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, trace, set_default_openai_client, set_tracing_disabled
import os
from openai import AsyncOpenAI
"""
Without the agents library: You manually build the list of messages (system prompt, history, user message) and then call openai.chat.completions.create() yourself. This is what you see in DocumentAnalyzerService.py.

With the agents library: The Agent object holds the instructions (which become the system prompt), and Runner.run takes care of the rest. It combines the agent's instructions with the user's message, makes the asynchronous await client.chat.completions.create(...) call behind the scenes, and manages the conversation flow.
"""

class PanditJI:
    def __init__(self):
        load_dotenv(override=True)
        open_router_key = os.getenv('OPEN_ROUTER_API_KEY')
        open_router_base_url = os.getenv('OPEN_ROUTER_BASE_URL')
        openai = AsyncOpenAI(api_key=open_router_key, base_url=open_router_base_url)
        set_default_openai_client(openai, use_for_tracing=False)
        set_tracing_disabled(True)

    async def create_agent(self):
         instruction = """You are a future predictor which predicts future on the basis of birth date. 
         You will get the birth date, time of birth as input, birth location along with birth country as input. 
         Please use it as input and use indian mythological methods to predict future and share complete kundli."""
         birthDate = input("Please enter your birth date: ")
         birthTime = input("Please enter your birth time: ")
         birthLocation = input("Please Enter your birth location:")
         birthCountry = input("Please Enter Country:")
         agent = Agent(name="Pandit Ji", instructions=instruction,  model="gpt-4o-mini")   
         user_input = f"Birth Date: {birthDate}, Birth Time: {birthTime}, BirthLocation: {birthLocation}, birthCountry: {birthCountry}"
         result = await Runner.run(agent, user_input)
         print(result.final_output)

if __name__ == "__main__":
    me = PanditJI()
    asyncio.run(me.create_agent())