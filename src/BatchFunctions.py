
# batch functions
# Gradio supports the ability to pass batch functions. Batch functions are just functions which take in a list of inputs and return a list of predictions.
# 16 requests could be processed in parallel 

import time
import platform
import gradio as gr

def trim_words(words, lens):
    trimmed_words = []
    time.sleep(5)
    for w, l in zip(words, lens):
        trimmed_words.append(w[:int(l)])
    return [trimmed_words]

with gr.Blocks().queue() as demo:
    with gr.Row():
        word = gr.Textbox(label="文字")
        leng = gr.Number(label="长度")
        output = gr.Textbox(label="输出")
    with gr.Row():
        run = gr.Button()

    event = run.click(trim_words, [word, leng], output, batch=True, max_batch_size=16)

if platform.system() == 'Windows':
    demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
else:
    demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)