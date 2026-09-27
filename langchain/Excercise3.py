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
    translatedResponse: str

@tool
def sendPushNotification():
    """Send a short pushnotification to user's phone"""
    print("Sending Notification")
    return "Notification Sent"    

def chat_with_llm(state: State):
    llm_with_Tools = llm.bind_tools([sendPushNotification])
    return {"messages":[llm_with_Tools.invoke(state["messages"])]}

def translatorNode(state: State):
    message = state["messages"][-1].content
    prompt = f"Translate this into Hindi, replying with the translation only:\n\n{message}"
    return {"translatedResponse": llm.invoke(prompt).content}
tools = [sendPushNotification]
memory = MemorySaver()
builder = StateGraph(State)
builder.add_node("chat_with_llm",chat_with_llm)
builder.add_node("tools", ToolNode(tools))
builder.add_node("translator", translatorNode)

builder.add_edge(START,"chat_with_llm")
builder.add_conditional_edges("chat_with_llm",tools_condition, {"tools": "tools", END: "translator"})
builder.add_edge("tools","chat_with_llm")
builder.add_edge("translator",END)

graph = builder.compile(checkpointer=memory)
result = graph.invoke({"messages": [{"role":"user", "content":"In one sentence say something about banana."}]})
print(result["messages"][-1].content)
print(result["translatedResponse"])