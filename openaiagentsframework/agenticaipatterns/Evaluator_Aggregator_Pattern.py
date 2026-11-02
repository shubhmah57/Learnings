import asyncio
from dotenv import load_dotenv
from agents import (
    Agent,
    ModelSettings,
    Runner,
    set_default_openai_client,
    set_tracing_disabled,
)
import os
from openai import AsyncOpenAI

class Evaluator_Aggregated_Pattern:
    def __init__(self):
        load_dotenv(override=True)
        open_router_key = os.getenv('OPEN_ROUTER_API_KEY')
        open_router_base_url = os.getenv('OPEN_ROUTER_BASE_URL')
        openai = AsyncOpenAI(api_key=open_router_key, base_url=open_router_base_url)
        set_default_openai_client(openai, use_for_tracing=False)
        set_tracing_disabled(True)

    async def perform_tasks(self):
        instructions1 = """You are a sales agent working for ComplAI,
        a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI.
        You write professional, serious cold emails."""

        instructions2 = """You are a humorous, engaging sales agent working for ComplAI,
        a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI.
        You write witty, engaging cold emails that are likely to get a response."""

        instructions3 = """You are a busy sales agent working for ComplAI,
        a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI.
        You write concise, to the point cold emails."""

        model_settings = ModelSettings(max_tokens=500)
        agent1 = Agent(
            name="Agent1",
            instructions=instructions1,
            model="gpt-4o-mini",
            model_settings=model_settings,
        )
        agent2 = Agent(
            name="Agent2",
            instructions=instructions2,
            model="gpt-4o-mini",
            model_settings=model_settings,
        )
        agent3 = Agent(
            name="Agent3",
            instructions=instructions3,
            model="gpt-4o-mini",
            model_settings=model_settings,
        )
        message = "Write A COld EMail"
        results = await asyncio.gather(Runner.run(agent1,message),Runner.run(agent2,message),Runner.run(agent3,message))
        output = [result.final_output for result in results]
        print(output)
        sales_picker = Agent(
            name="sales_picker",
            instructions=(
                "You pick the best cold sales email from the given options. "
                "Imagine you are a customer and pick the one you are most likely to respond to. "
                "Do not give an explanation; reply with the selected email only."
            ),
            model="gpt-4o-mini",
            model_settings=model_settings,
        )
        response = await Runner.run(sales_picker, str(output))
        print('*******************')
        print(response.final_output)
        print('*******************')

if __name__ == "__main__":
    object = Evaluator_Aggregated_Pattern()
    asyncio.run(object.perform_tasks())