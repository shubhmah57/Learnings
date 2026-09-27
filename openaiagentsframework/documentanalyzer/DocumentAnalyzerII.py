from pathlib import Path
import sys

# Gradio Default port is 7860
# Ensure workspace root is on sys.path so package imports work when
# running the script directly. The workspace root is two levels up
# from this file (udemy-ed-donner-ownpractice).
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from dotenv import load_dotenv
import openaiagentsframework.documentanalyzer.Evaluation as Evaluation
import gradio as gr
from utils import CommonUtils
import openaiagentsframework.documentanalyzer.DocumentAnalyzerService as DocumentAnalyzerService
import os


load_dotenv(override=True)

def evaluateResponse(message,history):

    api_key = os.getenv('OPEN_ROUTER_API_KEY')
    open_ai_base_url = os.getenv('OPEN_ROUTER_BASE_URL')
    open_ai = CommonUtils.getOpenAInstance(api_key,open_ai_base_url)
    system_prompt = DocumentAnalyzerService.buildSystemPrompt()
    if CommonUtils.is_blank(message):
        message = "Do you have a patent ?"
    messages = [{"role":"system", "content":system_prompt}] + [{"role":"user","content":message}]
    respone = open_ai.chat.completions.create(model="gpt-4o-mini",messages=messages,max_tokens=250)
    reply = respone.choices[0].message.content
    print(f"Reply is {reply}")
    user_prompt = build_user_prompt_toevaluate(reply,message,history)
    evaluator_message = [{"role":"system","content":system_prompt}] + [{"role":"user","content":user_prompt}]
    gemini_response= open_ai.chat.completions.parse(model="gemini-2.5-flash",messages=evaluator_message,max_tokens=250,response_format=Evaluation.Evaluation)
    gemini_reply = gemini_response.choices[0].message.parsed
    if gemini_reply.isAcceptable:
        return reply
    else:
        return "Incorrect Response"

def build_user_prompt_toevaluate(reply, message, history):
    user_prompt = f"Here's the conversation between the User and the Agent: \n\n{history}\n\n"
    user_prompt += f"Here's the latest message from the User: \n\n{message}\n\n"
    user_prompt += f"Here's the latest response from the Agent: \n\n{reply}\n\n"
    user_prompt += "Please evaluate the response, replying with whether it is acceptable and your feedback."
    return user_prompt

def chat(message, history):
    return evaluateResponse(message,history)

if __name__ ==  "__main__":
    #evaluateResponse()
    gr.ChatInterface(chat).launch()