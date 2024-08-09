
# Interface 方法

import time
import platform
import gradio as gr

def generator(x):
    for i in range(10):
        time.sleep(0.5)
        yield i

demo = gr.Interface(fn=generator, inputs="text", outputs="text", title="Yield程序", allow_flagging="never")

if platform.system() == 'Windows':
    demo.queue().launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
else:
    demo.queue().launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)