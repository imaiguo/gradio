
import platform
import gradio as gr
import random
import time

from loguru import logger

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    def user(user_message, history):
        return "", history + [[user_message, None]]

    def bot(history):
        logger.debug(f"history->{history}")
        # history->[['你好', 'I love you'], ['Fine', None]]
        bot_message = random.choice(["How are you?", "I love you", "I'm very hungry"])
        time.sleep(2)
        history[-1][1] = bot_message
        return history

    msg.submit(fn=user, inputs=[msg, chatbot], outputs=[msg, chatbot], queue=False).then(fn=bot, inputs=chatbot, outputs=chatbot)

    clear.click(fn=lambda: None, inputs=None, outputs=chatbot, queue=False)
    
demo.queue()
if platform.system() == 'Windows':
    demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
else:
    demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)
