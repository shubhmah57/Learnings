
import asyncio
from pathlib import Path

from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from IPython.display import Markdown, display

from utils.modelconfig import ModelConfig


class FirstProgram(ModelConfig):
    def __init__(self):
        super().__init__()

    async def main(self):
        instructions = (
            "Use the memory tools to persist and recall information about the user. "
            "When the user asks to remember information, save it using the memory tools "
            "before confirming."
        )
        request = (
            "Please save these facts using your memory tools: my name is Shubham; "
            "I am a senior software engineer, an enthusiastic learner, and I am "
            "always looking for new things to learn."
        )
        memory_path = Path(__file__).resolve().parent / "memory" / "memory.json"
        memory_path.parent.mkdir(parents=True, exist_ok=True)

        memory_params = {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-memory"],
            "env": {"MEMORY_FILE_PATH": str(memory_path)},
        }
        async with MCPServerStdio(
            params=memory_params, client_session_timeout_seconds=60
        ) as server:
            agent = Agent(
                name="agent",
                instructions=instructions,
                model=self.model,
                mcp_servers=[server],
            )
            result = await Runner.run(agent, request)
            display(Markdown(result.final_output))
        async with MCPServerStdio(
                    params=memory_params, client_session_timeout_seconds=60
                ) as retrive_server:
                    agent = Agent(
                        name="agent",
                        instructions=instructions,
                        model=self.model,
                        mcp_servers=[retrive_server],
                    )
                    result = await Runner.run(agent, "What was my name and am I enthusiastic about ?")    
                    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(FirstProgram().main())