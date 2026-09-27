import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, set_default_openai_client, set_tracing_disabled
import os
from openai import AsyncOpenAI

"""
Multi-Agent Orchestration Pattern:
Orchestrates multiple specialized sales agents to generate different variations 
of cold emails. A manager agent evaluates them and selects the best one to 
send using a simulated email tool.
"""


class Multi_Agent_Orchestration:
    def __init__(self):
        load_dotenv(override=True)
        open_router_key = os.getenv('OPEN_ROUTER_API_KEY')
        open_router_base_url = os.getenv('OPEN_ROUTER_BASE_URL')
        openai = AsyncOpenAI(api_key=open_router_key, base_url=open_router_base_url)
        set_default_openai_client(openai, use_for_tracing=False)
        set_tracing_disabled(True)

    async def performTasks(self):
        instructions1 = """You are a sales agent working for ComplAI,
        a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI.
        You write professional, serious cold emails."""

        instructions2 = """You are a humorous, engaging sales agent working for ComplAI,
        a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI.
        You write witty, engaging cold emails that are likely to get a response."""

        instructions3 = """You are a busy sales agent working for ComplAI,
        a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI.
        You write concise, to the point cold emails."""

        agent1 = Agent(name="Agent1", instructions= instructions1, model="gpt-4o-mini")
        agent2 = Agent(name="Agent2", instructions= instructions2, model="gpt-4o-mini")
        agent3 = Agent(name="Agent3", instructions= instructions3, model="gpt-4o-mini")
        description = "Write a cold sales email"
        tools = [agent1.as_tool(tool_name="agent1_tool", tool_description= description),agent2.as_tool(tool_name="agent2_tool", tool_description= description),agent3.as_tool(tool_name="agent3_tool",tool_description=description),self.send_email]
        instructions = """
        You are a Sales Manager at ComplAI. Your goal is to find the single best cold sales email using the sales_agent tools.
 
        Follow these steps carefully:
        1. Generate Drafts: Use all three sales_agent tools to generate three different email drafts. Do not proceed until all three drafts are ready.
 
        2. Evaluate and Select: Review the drafts and choose the single best email using your judgment of which one is most effective.
 
        3. Use the send_email tool to send the best email (and only the best email) to the user.
 
            Crucial Rules:
        - You must use the sales agent tools to generate the drafts — do not write them yourself.
        - You must send ONE email using the send_email tool — never more than one.
        """
        message = "Send a cold sales email addressed to 'Dear CEO'"
        sales_agent = Agent(name="Agent4", instructions= instructions, tools=tools, model="gpt-4o-mini")
        response = await Runner.run(sales_agent, message)
        


    @function_tool
    def send_email():
        print('Sending Email')

if __name__ == "__main__":
    object = Multi_Agent_Orchestration()
    asyncio.run(object.performTasks())
