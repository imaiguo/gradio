
import platform
import gradio as gr

from loguru import logger

def alternatingly_agree(message, history):
    logger.debug(f"history->{history}")
    if len(history) % 2 == 0:
        return f"Yes, I do think that '{message}'"
    else:
        return "I don't think so"

if platform.system() == 'Windows':
    gr.ChatInterface(fn=alternatingly_agree).launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
else:
    gr.ChatInterface(fn=alternatingly_agree).launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)