
import platform
import random
import gradio as gr

def random_response(message, history):
    return random.choice(["Yes", "No"])

if platform.system() == 'Windows':
    gr.ChatInterface(fn=random_response).launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
else:
    gr.ChatInterface(fn=random_response).launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)
