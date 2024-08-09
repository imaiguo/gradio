import platform
import gradio as gr
import numpy as np
import time

def fake_diffusion(steps):
    rng = np.random.default_rng()
    for i in range(steps):
        time.sleep(1)
        image = rng.random(size=(1000, 1000, 3))
        yield image

    image = np.ones((1000,1000,3), np.uint8)
    image[:] = [255, 124, 0]
    yield image

# gr.Slider的返回值作为fake_diffusion的参数steps
demo = gr.Interface(fake_diffusion, inputs=gr.Slider(1, 10, 3, step=1), outputs="image", theme=gr.themes.Monochrome()).queue()

if platform.system() == 'Windows':
    demo.queue().launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
else:
    demo.queue().launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)
