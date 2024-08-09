import platform
import gradio as gr

# themes list:
# gr.themes.Base()
# gr.themes.Default()
# gr.themes.Glass()
# gr.themes.Monochrome()
# gr.themes.Soft()


# with gr.Blocks(css=".gradio-container {background-color: blue}") as demo:
with gr.Blocks(css=".gradio-container {background: url('file=images/Einstein.jpg')}") as demo:
    with gr.Row():
        btn1 = gr.Button("Button 1")
        btn2 = gr.Button("Button 2")

if platform.system() == 'Windows':
    demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False, allowed_paths=["images"])
else:
    demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False, allowed_paths=["images\Einstein.jpg"])