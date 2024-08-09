
import platform
import gradio as gr

from transformers import pipeline

pipe = pipeline("translation", model="t5-base")


def translate(text):
    return pipe(text)[0]["translation_text"]


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            english = gr.Textbox(label="English text")
            translate_btn = gr.Button(value="Translate")
        with gr.Column():
            german = gr.Textbox(label="German Text")

    translate_btn.click(translate, inputs=english, outputs=german, api_name="translate-to-german")
    examples = gr.Examples(examples=["I went to the supermarket yesterday.", "Helen is a good swimmer."],
                           inputs=[english])

if platform.system() == 'Windows':
    demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
else:
    demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)