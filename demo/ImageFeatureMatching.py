
import gradio as gr

from loguru import logger

def showFile(file1, file2):
    logger.debug(f"file.name:{file1}")
    logger.debug(f"file.name:{file2}")
    return gr.Image(visible=True, value=file2)

with gr.Blocks(title="图片特征比较", css="footer {visibility: hidden}") as demo:
    with gr.Row():
        imageOutput1 = gr.Image(label="图片1", width=500, height=500)
        imageOutput2 = gr.Image(label="图片2", width=500, height=500)
    imageOutput3 = gr.Image(label="比较结果", visible=False, width=1000, height=500)
    
    submitButton = gr.Button("图像特征比较", min_width=1, variant="primary")

    submitButton.click(fn=showFile, inputs=[imageOutput1, imageOutput2], outputs=[imageOutput3], queue=False)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8000, inbrowser=False, share=False)
