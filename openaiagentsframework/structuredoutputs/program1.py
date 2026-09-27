from pydantic import BaseModel, Field
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from agents import Agent, Runner, trace, set_default_openai_client, set_tracing_disabled
import asyncio

email= """
        Hi [first_name],
        I'm hitting you up to see if you'd like to buy our product. It's realy great. You will miss out if you don't buy it.
        
        Laters.

        Shubham
            """

class EmailReview(BaseModel):
    is_professional: bool = Field(description="Whether the email is professional and appropriate")
    number_of_sentences: int =  Field(description="The number of sentences in email")
    contains_placeholder: bool = Field(description= "Whether the email contains the placeholder for personalization")


class program1:



    def __init__(self):
        load_dotenv(override=True)
        open_router_key = os.getenv('OPEN_ROUTER_API_KEY')
        open_router_base_url = os.getenv('OPEN_ROUTER_BASE_URL')
        openai = AsyncOpenAI(api_key=open_router_key, base_url=open_router_base_url)
        set_default_openai_client(openai, use_for_tracing=False)
        set_tracing_disabled(True)


    async def  call_agent(self):
        agent = Agent(name="Email Review Agent", instructions="You review potential emails", model="gpt-4o-mini", output_type=EmailReview)
        result = await Runner.run(agent, email)
        review = result.final_output
        print(review)


if __name__ == "__main__":
    object = program1()
    asyncio.run(object.call_agent())