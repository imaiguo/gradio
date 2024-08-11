
import gradio as gr

from loguru import logger

def showFile(file1):
    logger.debug(f"Get File")
    return gr.Image(visible=True, value=file1)

with gr.Blocks(title="图片特征比较", css="footer {visibility: hidden}") as demo:
    with gr.Row():
        imageOutput1 = gr.Image(label="图片", width=500, height=500)
        imageOutput2 = gr.Image(label="图片特征", width=500, height=500, visible=False, sources = None)

    submitButton = gr.Button("图像特征比较", min_width=1, variant="primary")

    submitButton.click(fn=showFile, inputs=[imageOutput1], outputs=[imageOutput2], queue=False)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8000, inbrowser=False, share=False)
