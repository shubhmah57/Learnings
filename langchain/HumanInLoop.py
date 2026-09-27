from langchain_core.tools import tool
# Imports and environment first

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from langchain_openai import ChatOpenAI
import os
load_dotenv(override=True)


model = ChatOpenAI(
    model="openrouter/free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_ROUTER_API_KEY"),
    max_completion_tokens= 1000
)
@tool
def book_meeting(person: str, day: str) -> str:
    """Book a meeting with a person on a given day."""
    return f"Meeting booked with {person} on {day}."

approval_agent = create_agent(
    model=model,
    tools=[book_meeting],
    system_prompt="You are a scheduling assistant. Use the book_meeting tool.",
    middleware=[HumanInTheLoopMiddleware(interrupt_on={"book_meeting": True})],
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": "approval-demo"}}
result = approval_agent.invoke(
    {"messages": [{"role": "user", "content": "Book a meeting with Sam on Friday."}]}, config
)

interrupt = result["__interrupt__"][0]
print("The agent paused and is asking for approval:")
print(interrupt.value["action_requests"][0]["description"])

resumed = approval_agent.invoke(Command(resume={"decisions": [{"type": "approve"}]}), config)
print(resumed["messages"][-1].content)