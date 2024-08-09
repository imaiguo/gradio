
import platform
import gradio as gr

def store_message(message: str, history: list[str]):
    output = {
        "Current messages": message,
        "Previous messages": history[::-1]
    }
    history.append(message)
    return output, history

demo = gr.Interface(fn=store_message, 
                    inputs=["textbox", gr.State(value=[])], 
                    outputs=["json", gr.State()])

if platform.system() == 'Windows':
    demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
else:
    demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)