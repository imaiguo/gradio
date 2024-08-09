
import platform
import random
import string
import gradio as gr 

def save_image_random_name(image):
    random_string = ''.join(random.choices(string.ascii_letters, k=20)) + '.png'
    image.save("save." + random_string)
    print(f"Saved image to {random_string}!")

demo = gr.Interface(
    fn=save_image_random_name, 
    inputs=gr.Image(type="pil"), 
    outputs=None,
)

if platform.system() == 'Windows':
    demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
else:
    demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)
