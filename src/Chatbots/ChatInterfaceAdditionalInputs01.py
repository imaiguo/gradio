
import platform
import gradio as gr
import time

def echo(message, history, system_prompt, tokens):
    response = f"System prompt: {system_prompt}\n Message: {message}."
    for i in range(min(len(response), int(tokens))):
        time.sleep(0.05)
        yield response[: i+1]

demo = gr.ChatInterface(fn=echo, 
                        additional_inputs=[
                            gr.Textbox("You are helpful AI.", label="System Prompt"), 
                            gr.Slider(10, 100)
                        ]
                       ).queue()

if __name__ == "__main__":
    if platform.system() == 'Windows':
        demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
    else:
        demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)