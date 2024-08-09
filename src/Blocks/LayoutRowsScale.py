
# The widths of elements in a Row can be controlled via a combination of scale and min_width arguments that are present in every Component.

import platform
import gradio as gr

with gr.Blocks() as demo:
    with gr.Row():
        btn0 = gr.Button("Button 0", scale=0)
        btn1 = gr.Button("Button 1", scale=1)
        btn2 = gr.Button("Button 2", scale=2)

if platform.system() == 'Windows':
    demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
else:
    demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)