
import platform
import gradio as gr
import random
import time

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.ClearButton(components=[msg, chatbot])

    def respond(message, chat_history):
        bot_message = random.choice(["How are you?", "I love you", "I'm very hungry"])
        chat_history.append((message, bot_message))
        time.sleep(2)
        return "", chat_history

    msg.submit(fn=respond, inputs=[msg, chatbot], outputs=[msg, chatbot])

if platform.system() == 'Windows':
    demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
else:
    demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)