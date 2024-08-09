# 程序运行命令
# uvicorn.exe FastAPI:app --host 192.168.2.198 --port 8001

from fastapi import FastAPI
import gradio as gr

CUSTOM_PATH = "/gradio"

app = FastAPI(title="Fast和Gradio融合展示")


@app.get("/")
def read_main():
    return {"message": "This is your main app"}


io = gr.Interface(lambda x: "Hello, " + x + "!", "textbox", "textbox")
app = gr.mount_gradio_app(app, io, path=CUSTOM_PATH)

# Run this from the terminal as you would normally start a FastAPI app: `uvicorn run:app`
# and navigate to http://localhost:8000/gradio in your browser.
