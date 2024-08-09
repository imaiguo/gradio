
import platform
import gradio as gr

css = """
#warning {background-color: #FFCCCB}
.feedback textarea {font-size: 24px !important}
"""

with gr.Blocks(css=css) as demo:
    box1 = gr.Textbox(value="Good Job", elem_classes="feedback")
    box2 = gr.Textbox(value="Failure", elem_id="warning", elem_classes="feedback")

if platform.system() == 'Windows':
    demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False, allowed_paths=["images\Einstein.jpg"])
else:
    demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False, allowed_paths=["images\Einstein.jpg"])