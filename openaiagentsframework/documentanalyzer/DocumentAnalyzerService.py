from pathlib import Path
from dotenv import load_dotenv
from utils import CommonUtils
import os
import gradio as gr
from pathlib import Path

load_dotenv(override=True)

#import sys
## This hack is used for directly running from this class to help with relative imports
#ROOT_DIR = Path(__file__).resolve().parents[1]
#if str(ROOT_DIR) not in sys.path:
#    sys.path.insert(0, str(ROOT_DIR))



def chat(message, history):
    api_key = os.getenv('OPEN_ROUTER_API_KEY')
    base_url = os.getenv('OPEN_ROUTER_BASE_URL')
    openai = CommonUtils.getOpenAInstance(api_key,base_url)
    system_prompt = buildSystemPrompt()

    messages = [{"role":"system","content":system_prompt}] + history + [{"role":"user","content":message}]
    response = openai.chat.completions.create(model="gpt-4o-mini",messages=messages,max_tokens=2000)
    
    return response.choices[0].message.content

def buildSystemPrompt():
    pdf_path = Path(__file__).resolve().parent / "resources" / "linkedin.pdf"
    linkedin = CommonUtils.readPDFfile(str(pdf_path))
    name = "Ed Donner"
    summary = ""
    summary_path = Path(__file__).resolve().parent/"resources" / "summary.txt"
    strPath = str(summary_path)
    with open(strPath,"r",encoding="utf-8") as f:
        summary = f.read()
    #print(f"Summary is:{summary}")    
    
    ## Build System Prompt
    system_prompt = f"You are acting as {name}. You are answering questions on {name}'s website, \
    particularly questions related to {name}'s career, background, skills and experience. \
    Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
    You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
    Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
    If you don't know the answer, say so."
    system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linkedin}\n\n"
    system_prompt += f"With this context, please chat with the user, always staying in character as {name}."
    return system_prompt


