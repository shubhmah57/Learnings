import gradio as gr
from openaiagentsframework.documentanalyzer.DocumentAnalyzerService import chat


if __name__ == "__main__":
    gr.ChatInterface(chat).launch()