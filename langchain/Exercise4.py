from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
import os, sys
import asyncio
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv(override=True)


if sys.platform == "win32":
    import subprocess
    from functools import partial
    import langchain_mcp_adapters.sessions as mcp_sessions

    mcp_sessions.stdio_client = partial(mcp_sessions.stdio_client, errlog=subprocess.DEVNULL)
    print("Applied the Windows adjustment")
else:
    print("Not Windows, so nothing to do here")

groq_llm = ChatGroq(
    model="meta-llama/llama-4-maverick-17b-128e-instruct",  # ← try this first
    api_key=os.getenv("GROQ_API_KEY"),
    max_tokens=1000
)

llm = ChatOpenAI(
    model="openrouter/free",   # ← auto-picks a free model that supports tools
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_ROUTER_API_KEY"),
    max_tokens=1000
)

google_llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    max_output_tokens=1000
)
@wrap_tool_call
def log_tool_calls(request, handler):
    call = request.tool_call
    print(f"  [middleware] calling {call['name']} with {call['args']}")
    return handler(request)

client = MultiServerMCPClient({
    "playwright": {
        "transport": "stdio",
        "command": "npx",
        "args": ["-y", "@playwright/mcp@latest"],
    }
})

from langchain.agents.middleware import wrap_tool_call

BLOCKLIST = {"facebook.com", "twitter.com", "x.com"}


def is_blocked(url: str) -> bool:
    return any(blocked in url for blocked in BLOCKLIST)

@wrap_tool_call
def blocklist_middleware(request, handler):
    tool_name = request.tool_call["name"]
    args = request.tool_call.get("args", {})

    # Only check navigation tool
    if tool_name == "browser_navigate":
        url = args.get("url", "")
        
        if is_blocked(url):
            print(f"\n BLOCKED: {url}")
            # return fake response — tool never actually called
            return "Navigation blocked: this site is on the blocklist."
    
    # Everything else — pass through normally
    print(f"\n ALLOWED: {tool_name}")
    return handler(request)

async def main():
    browserTools = await client.get_tools()
    agent = create_agent(
        model = google_llm,
        tools = browserTools,
        system_prompt="You are a web research assistant. Use the browser tools to complete the task, then report clearly.",
        checkpointer=MemorySaver()
    )

    config = {"configurable": {"thread_id": "browser_tracking"}}
    message = {"messages": [{"role": "user","content": "Go to https://github.com/trending and list the top 2 repositories: name, short description, and primary language (if shown)."}]}
    result =  await agent.ainvoke(message, config=config)
    print("\n----Result")
    # print(result['messages'][-1].content)*/

    message1 = {"messages": [{"role": "user","content": "What is the primary language out of the top most repository ?"}]}
    result1 =  await agent.ainvoke(message1, config=config)
    print("\n----Result")
    print(result1['messages'][-1].content)

    # TODO: Middleware doesn't works, need to check why it doesn't work
    # agent = create_agent(
    #         model = google_llm,
    #         tools = browserTools,
    #         middleware= blocklist_middleware,
    #         system_prompt="You are a web research assistant. Use the browser tools to complete the task, then report clearly.",
    #         checkpointer=MemorySaver()
    # )

    # config = {"configurable": {"thread_id": "browser_tracking"}}
    # message = {"messages": [{"role": "user","content": "Go to https://facebook.com and what you see over there?"}]}
    # result =  await agent.ainvoke(message, config=config)
    # print("\n----Result")
    # # print(result['messages'][-1].content)*/

    # message1 = {"messages": [{"role": "user","content": "What is the primary language out of the top most repository ?"}]}
    # result1 =  await agent.ainvoke(message1, config=config)
    # print("\n----Result")
    # print(result1['messages'][-1].content)    

if __name__ == "__main__":
    asyncio.run(main())