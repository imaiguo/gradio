
import platform
import gradio as gr

def increase(num):
    return num + 1

with gr.Blocks() as demo:
    a = gr.Number(label="a")
    b = gr.Number(label="b")
    atob = gr.Button("a > b")
    btoa = gr.Button("b > a")
    atob.click(increase, a, b)
    btoa.click(increase, b, a)

if platform.system() == 'Windows':
    demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
else:
    demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)