
import platform
import gradio as gr

from transformers import pipeline

# https://huggingface.co/spaces/gradio/english_translator
english_translator = gr.load(name="spaces/gradio/english_translator")
english_generator = pipeline("text-generation", model="distilgpt2")


def generate_text(text):
    english_text = english_generator(text)[0]["generated_text"]
    german_text = english_translator(english_text)
    return english_text, german_text


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            seed = gr.Text(label="Input Phrase")
        with gr.Column():
            english = gr.Text(label="Generated English Text")
            german = gr.Text(label="Generated German Text")
    btn = gr.Button("Generate")
    btn.click(generate_text, inputs=[seed], outputs=[english, german])
    gr.Examples(["My name is Clara and I am"], inputs=[seed])

if platform.system() == 'Windows':
    demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
else:
    demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)