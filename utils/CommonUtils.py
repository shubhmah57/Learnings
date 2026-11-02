from openai import OpenAI
from pypdf import PdfReader

def getOpenAInstance(key,baseurl):
    opeai = OpenAI(api_key=key,base_url=baseurl)
    return opeai

def readPDFfile(path):
    reader = PdfReader(path)
    content =""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            content += text
    return content

def is_blank(s):
    return not s or s.strip() == ""        