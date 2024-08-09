
import platform
import time
import gradio as gr

def slow_echo(message, history):
    for i in range(len(message)):
        time.sleep(0.3)
        yield "You typed: " + message[: i+1]

if platform.system() == 'Windows':
    gr.ChatInterface(fn=slow_echo).launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
else:
    gr.ChatInterface(fn=slow_echo).launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)