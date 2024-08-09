
import platform
import gradio as gr

with gr.Blocks() as demo:
    with gr.Row():
        num1 = gr.Slider(1, 10)
        num2 = gr.Slider(1, 10)
        num3 = gr.Slider(1, 10)
    output = gr.Number(label="Sum")

    @gr.on(inputs=[num1, num2, num3], outputs=output)
    def sum(a, b, c):
        return a + b + c

if platform.system() == 'Windows':
    demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
else:
    demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)
