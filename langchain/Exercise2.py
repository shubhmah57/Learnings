import os
import random
import requests
from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv
import gradio as gr
from langchain_openai import ChatOpenAI
from langchain_community.tools import GoogleSerperRun
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

load_dotenv(override=True)

llm= ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_ROUTER_API_KEY"),
    max_completion_tokens= 1000
)
class State(TypedDict):
    messages: Annotated[list, add_messages]

nouns = ["Cabbages", "Unicorns", "Toasters", "Penguins", "Bananas", "Eels", "Pickles"]
adjectives = ["outrageous", "smelly", "pedantic", "existential", "sparkly", "haunted"]

def chat_botmessage(state: State)-> dict:
    sentence = f"{random.choice(nouns)} are {random.choice(adjectives)}"
    return {"messages": [{"role":"assistant", "content":sentence}]}  

def chatbot_node(state: State):
    return {"messages": [llm.invoke(state["messages"])]}    

builder = StateGraph(State)
builder.add_node("silly",chat_botmessage)
builder.add_edge(START,"silly")
builder.add_edge("silly",END)
graph = builder.compile()

result = graph.invoke({"messages": [{"role":"user", "content": "say something"}]})
resu = {'messages': [HumanMessage(content='say something', additional_kwargs={}, response_metadata={}, id='23f76412-5e1e-43c8-8965-f8d615914a5a'), AIMessage(content='Unicorns are smelly', additional_kwargs={}, response_metadata={}, id='ee881f11-8b1e-4a6d-88e8-e421c2468043', tool_calls=[], invalid_tool_calls=[])]}
print(result["messages"][-1].content)


builder1 = StateGraph(State)
builder1.add_node("silly1",chatbot_node)
builder1.add_edge(START,"silly1")
builder1.add_edge("silly1",END)
graph1 = builder1.compile()

result1 = graph1.invoke({"messages": [{"role":"user", "content": "say something"}]})
print(result1["messages"][-1].content)

## Using Tools 
## The "Cheat Sheet" Summarybind_tools(): Registers functions with the LLM so it knows its options.
# tools_condition: The automated if/else decider ("Did the LLM request a tool call or not?").
# ToolNode: The executioner ("No manual parsing needed; I unpack arguments, run the function, and format the output").


@tool
def send_push_notification(text: str) -> str:
    """Send a short push notification to the user's phone."""
    #requests.post(
    #    "https://api.pushover.net/1/messages.json",
    #    data={"token": os.getenv("PUSHOVER_TOKEN"), "user": os.getenv("PUSHOVER_USER"), "message": text},
    #)
    return "Notification sent"

tools = [send_push_notification]
llm_with_tools = llm.bind_tools(tools)

def chat_bot_node_with_tools(state: State):
    return {"messages":[llm_with_tools.invoke(state["messages"])]}

builder_tools = StateGraph(State)
builder_tools.add_node("chatbotnode",chat_bot_node_with_tools)
builder_tools.add_node("tools",ToolNode(tools))

builder_tools.add_edge(START,"chatbotnode")
builder_tools.add_conditional_edges("chatbotnode", tools_condition)
builder_tools.add_edge("tools", "chatbotnode")
graph = builder_tools.compile()

result = graph.invoke({"messages": [{"role": "user", "content": "Tell me the ingredients in banoffee pie and send me a push notification."}]})
print(result["messages"][-1].content)