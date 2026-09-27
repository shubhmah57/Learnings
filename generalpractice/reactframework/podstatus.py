from pathlib import Path
import sys
import json
from dotenv import load_dotenv

# Ensure workspace root is on sys.path so `utils` imports resolve when
# running this script directly.
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from utils import CommonUtils
import os
load_dotenv(override=True)

apikey = os.getenv('OPEN_ROUTER_API_KEY')
baseURL = os.getenv('OPEN_ROUTER_BASE_URL')

openai = CommonUtils.getOpenAInstance(apikey,baseURL)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_pod_status",
            "description": "Returns the status of a Kubernetes pod",
            "parameters": {
                "type": "object",
                "properties": {
                    "pod_name": {"type": "string"}
                },
                "required": ["pod_name"],
            },
        },
    }
]

def executeTool(name:str, args:dict)->str:
    """Mock Execution of tool"""
    if name == "get_pod_status":
        return json.dumps({"pod": args["pod_name"], "status":"CrashLoopBackOff", "restarts":14})
    return json.dumps({"error":"Unkown Tool"})

messages = [{"role":"user", "content":"Why is the auth-service pod failing ?"}]
# messages = [{"role":"user", "content":"What is BRICS SUMMIT ?"}]


maxIterations = 5

for iteration in range(maxIterations):
    response = openai.chat.completions.create(model= "gpt-4o-mini",messages=messages,max_tokens=500,tools=tools)

    choice = response.choices[0].message
    messages.append(choice)

    if not choice.tool_calls:
        print(f"Final Answer:{choice.content}")
        break

    for tool_call in choice.tool_calls:
        print("Inside Tool Call Loop")
        fn_name = tool_call.function.name
        fn_args = json.loads(tool_call.function.arguments)

        tool_output = executeTool(fn_name,fn_args)

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": tool_output
        })
