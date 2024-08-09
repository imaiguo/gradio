
# Interface 方法

import platform
import gradio as gr

def greet(name):
    return "Hello " + name + "!"

demo = gr.Interface(fn=greet, inputs="text", outputs="text", title="Interface程序", allow_flagging="never")

if platform.system() == 'Windows':
    demo.queue().launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
else:
    demo.queue().launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)