import platform
import gradio as gr

def generate_fake_image(prompt, seed, initial_image=None):
    return f"Used seed: {seed}", "https://dummyimage.com/300/09f.png"


demo = gr.Interface(
    generate_fake_image,
    inputs=["textbox"],
    outputs=["textbox", "image"],
    additional_inputs=[
        gr.Slider(0, 1000),
        "image"
    ]
)

if platform.system() == 'Windows':
    demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
else:
    demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)