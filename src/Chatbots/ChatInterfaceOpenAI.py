import os
import gradio as gr
import platform

from openai import OpenAI

if platform.system() == 'Windows':
    netip="192.168.2.198"
else:
    netip="192.168.2.200"

client = OpenAI(base_url=f"http://{netip}:9001/v1", api_key = "not need key")

def predict(message, history):
    history_openai_format = []
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human })
        history_openai_format.append({"role": "assistant", "content":assistant})

    history_openai_format.append({"role": "user", "content": message})
  
    response = client.chat.completions.create(model='gpt-3.5-turbo',
    messages= history_openai_format,
    temperature=1.0,
    stream=True)

    partial_message = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
              partial_message = partial_message + chunk.choices[0].delta.content
              yield partial_message


chatbot=gr.Chatbot(
            [],
            height=750,
            bubble_full_width=False,
            avatar_images=((os.path.join(os.path.dirname(__file__), "../../image/Einstein.jpg")), (os.path.join(os.path.dirname(__file__), "../../image/openai.png")))
        )

demo=gr.ChatInterface(fn=predict, title="LLM演示", chatbot=chatbot)

if __name__ == "__main__":
    if platform.system() == 'Windows':
        demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
    else:
        demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)