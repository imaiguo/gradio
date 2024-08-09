
import platform
import gradio as gr
import numpy as np

def flip(im):
    return np.flipud(im)

demo = gr.Interface(
    flip, 
    gr.Image(sources=["webcam"], streaming=True), 
    "image",
    live=True
)

if platform.system() == 'Windows':
    demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
else:
    demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)
