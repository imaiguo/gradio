import platform
import gradio as gr

css = """
.container {
    height: 100vh;
}
"""

with gr.Blocks(css=css) as demo:
    with gr.Column(elem_classes=["container"]):
        name = gr.Chatbot(value=[["1", "2"]], height="100%")

if platform.system() == 'Windows':
    demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
else:
    demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)