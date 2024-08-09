
import platform
import gradio as gr

with gr.Blocks() as demo:
    with gr.Row(equal_height=True):
        textbox = gr.Textbox()
        btn2 = gr.Button("Button 2")

if platform.system() == 'Windows':
    demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
else:
    demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)

