
import platform
import gradio as gr

# gradio >= 4.8.0
print(gr.__version__)

with gr.Blocks() as demo:
    im = gr.ImageEditor(
        width="50vw",
    )

if platform.system() == 'Windows':
    demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
else:
    demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)