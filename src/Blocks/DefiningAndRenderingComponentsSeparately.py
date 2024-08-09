
import platform
import gradio as gr

input_textbox = gr.Textbox()

with gr.Blocks() as demo:
    gr.Examples(["hello", "bonjour", "merhaba"], input_textbox)
    input_textbox.render()

if __name__ == "__main__":
    if platform.system() == 'Windows':
        demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
    else:
        demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)