import asyncio
import os
from pathlib import Path
from agents import (
    Agent,
    ModelSettings,
    Runner)
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv
from utils.modelconfig import ModelConfig

INSTRUCTIONS = """
Research the requested recipe on the web and return a concise Markdown summary
with the source URL. Do not claim to save a file.
"""

BROWSER_TOOLS = {
    "allowed_tool_names": [
        "browser_navigate",
        "browser_click",
        "browser_wait_for",
    ]
}
class firstprogrram(ModelConfig):
    def __init__(self):
        super().__init__()

    async def main(self) -> None:
        load_dotenv(override=True)

        sandbox_path = Path(__file__).resolve().parent / "sandbox"
        sandbox_path.mkdir(parents=True, exist_ok=True)

        playwright_params = {
        "command": "cmd",
        "args": ["/c", "npx", "-y", "@playwright/mcp@latest"],
        }

        async with MCPServerStdio(
            params=playwright_params,
            client_session_timeout_seconds=60,
            tool_filter=BROWSER_TOOLS,
        ) as mcp_server_browser:
            task = (
            "Find a great Bombay Sandwich recipe, verify its ingredients and "
            "method from a web source, and return a concise Markdown recipe "
            "with the source URL."
            )
            agent = Agent(
                name="investigator",
                instructions=INSTRUCTIONS,
                model=self.model,
                mcp_servers=[mcp_server_browser],
                model_settings=ModelSettings(max_tokens=1000),
            )
            result = await Runner.run(agent, task, max_turns=10)
            markdown = result.final_output
            if not markdown or not markdown.strip():
                raise RuntimeError("The agent returned no recipe Markdown to save.")

            output_path = sandbox_path / "banoffee.md"
            output_path.write_text(markdown, encoding="utf-8")
            print(f"Recipe saved to: {output_path}")


if __name__ == "__main__":
    asyncio.run(firstprogrram().main())
