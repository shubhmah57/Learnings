from agents import Agent, Runner, trace, set_default_openai_client, set_tracing_disabled, ModelSettings, OpenAIChatCompletionsModel
from dotenv import load_dotenv
from openai import AsyncOpenAI
import os
class ModelConfig:
    def __init__(self):
        load_dotenv(override=True)
        open_router_key = os.getenv("OPEN_ROUTER_API_KEY")
        open_router_base_url = os.getenv("OPEN_ROUTER_BASE_URL")
        openai = AsyncOpenAI(api_key=open_router_key,base_url=open_router_base_url)
        set_default_openai_client(openai)
        set_tracing_disabled(True)
        self.model_settings = ModelSettings(max_tokens=20000)
        
        self.model = OpenAIChatCompletionsModel(
                   model="openrouter/free",
                   openai_client= openai
            )