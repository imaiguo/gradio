import platform
import gradio as gr
import time

def slowly_reverse(word, progress=gr.Progress()):
    progress(0, desc="开始")
    time.sleep(2)
    progress(0.05)
    new_string = ""
    for letter in progress.tqdm(word, desc="转换中..."):
        time.sleep(0.25)
        # 实现文字倒序
        new_string = letter + new_string
    return new_string

demo = gr.Interface(slowly_reverse, gr.Text(), gr.Text())

if platform.system() == 'Windows':
    demo.queue().launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
else:
    demo.queue().launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)
