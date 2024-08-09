
import platform
import gradio as gr

def yes_man(message, history):
    if message.endswith("?"):
        return "Yes"
    else:
        return "Ask me anything!"

chatbot = gr.ChatInterface(
    fn=yes_man,
    chatbot=gr.Chatbot(height=600),
    textbox=gr.Textbox(placeholder="Ask me a yes or no question", container=False, scale=7),
    title="Yes Man",
    description="Ask Yes Man any question",
    theme="soft",
    examples=["Hello", "Am I cool?", "Are tomatoes vegetables?"],
    cache_examples=True,
    retry_btn=None,
    undo_btn="Delete Previous",
    clear_btn="Clear",
)

if platform.system() == 'Windows':
    chatbot.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
else:
    chatbot.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)