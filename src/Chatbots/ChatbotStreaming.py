


# 1. The first method user() updates the chatbot with the user message and clears the input field. This method also makes the input field non interactive so that the user can’t send another message while the chatbot is responding. Because we want this to happen instantly, we set queue=False, which would skip any queue had it been enabled. The chatbot’s history is appended with (user_message, None), the None signifying that the bot has not responded.

# 2. The second method, bot() updates the chatbot history with the bot’s response. Instead of creating a new message, we just replace the previously-created None message with the bot’s response. Finally, we construct the message character by character and yield the intermediate outputs as they are being constructed. Gradio automatically turns any function with the yield keyword into a streaming output interface.

# 3. The third method makes the input field interactive again so that users can send another message to the bot.

import platform
import gradio as gr
import random
import time

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(height=700, bubble_full_width=False)
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    def user(user_message, history):
        return "", history + [[user_message, None]]

    def bot(history):
        bot_message = random.choice(["How are you?", "I love you", "I'm very hungry"])
        history[-1][1] = ""
        for character in bot_message:
            history[-1][1] += character
            time.sleep(0.05)
            yield history

    msg.submit(fn=user, inputs=[msg, chatbot], outputs=[msg, chatbot], queue=False).then(
        fn=bot, inputs=chatbot, outputs=chatbot
    )

    clear.click(fn=lambda: None, inputs=None, outputs=chatbot, queue=False)
    
demo.queue()

if __name__ == "__main__":
    if platform.system() == 'Windows':
        demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
    else:
        demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)
