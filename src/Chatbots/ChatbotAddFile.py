
import platform
import gradio as gr
import os
import time

from loguru import logger

# Chatbot demo with multimodal input (text, markdown, LaTeX, code blocks, image, audio, & video). Plus shows support for streaming text.

def print_like_dislike(x: gr.LikeData):
    print(x.index, x.value, x.liked)

def add_text(history, text):
    history = history + [(text, None)]
    # interactive=False 设置输入对话框 禁止交互
    return history, gr.Textbox(value="", interactive=False)

def add_file(history, file):
    logger.debug(f"file.name:{file.name}")
    history = history + [((file.name,), None)]
    return history

def bot(history):
    response = "**That's cool!**"
    history[-1][1] = ""
    for character in response:
        history[-1][1] += character
        time.sleep(0.1)
        yield history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        [],
        height=800,
        elem_id="chatbot",
        bubble_full_width=False,
        avatar_images=((os.path.join(os.path.dirname(__file__), "../../image/Einstein.jpg")), (os.path.join(os.path.dirname(__file__), "../../image/openai.png")))
    )

    with gr.Row():
        txt = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Enter text and press enter, or upload an image",
            container=False,
        )

        btn = gr.UploadButton("📁", file_types=["image", "video", "audio"])

    txt_msg = txt.submit(fn=add_text, inputs=[chatbot, txt], outputs=[chatbot, txt], queue=False).then(fn=bot, inputs=chatbot, outputs=chatbot, api_name="bot_response")

    # interactive=False 设置输入对话框 可以交互
    txt_msg.then(fn=lambda: gr.Textbox(interactive=True), inputs=None, outputs=[txt], queue=False)

    file_msg = btn.upload(fn=add_file, inputs=[chatbot, btn], outputs=[chatbot], queue=False).then(fn=bot, inputs=chatbot, outputs=chatbot)

    chatbot.like(fn=print_like_dislike, inputs=None, outputs=None)

demo.queue()

if __name__ == "__main__":
    if platform.system() == 'Windows':
        demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
    else:
        demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)