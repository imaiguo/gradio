
import platform
import gradio as gr

from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage


if platform.system() == 'Windows':
    netip="192.168.2.198"
else:
    netip="192.168.2.200"

llm = ChatOpenAI(temperature=1.0, base_url=f"http://{netip}:9001/v1", api_key = "not need key")

def predict(message, history):
    history_langchain_format = []
    for human, ai in history:
        history_langchain_format.append(HumanMessage(content=human))
        history_langchain_format.append(AIMessage(content=ai))
    history_langchain_format.append(HumanMessage(content=message))
    gpt_response = llm(history_langchain_format)
    return gpt_response.content

demo=gr.ChatInterface(predict)

if __name__ == "__main__":
    if platform.system() == 'Windows':
        demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
    else:
        demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)