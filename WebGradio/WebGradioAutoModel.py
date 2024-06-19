
import os
import platform
import gradio as gr

from loguru import logger
from transformers import AutoModel, AutoTokenizer
from dotenv import load_dotenv

load_dotenv()

BindLocalIP = os.getenv('LocalIP')
BindPort = os.getenv('BindPort')
OpenAiPort = os.getenv('OpenAiPort')
GradioUser = os.getenv('GradioUser')
GradioPassword = os.getenv('GradioPassword')

print(f"BindLocalIP: {BindLocalIP}")
print(f"BindPort: {BindPort}")
print(f"OpenAiPort: {OpenAiPort}")
print(f"GradioUser: {GradioUser}")
print(f"GradioPassword: {GradioPassword}")

OpenAiServer=f"{BindLocalIP}:{OpenAiPort}"

if platform.system() == 'Windows':
    os.environ['PATH'] = os.environ.get("PATH", "") + os.pathsep + r'D:\devtools\PythonVenv\chatglb3\Lib\site-packages\torch\lib'

MODEL_PATH="/opt/Data/ModelWeight/THUDM/chatglm3-6b"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)

if platform.system() == 'Windows':
    model = AutoModel.from_pretrained(MODEL_PATH, trust_remote_code=True).quantize(8).to("cuda").eval()
else:
    model = AutoModel.from_pretrained(MODEL_PATH, trust_remote_code=True).to("cuda").eval()

def predict(chatbot, history):
    input = chatbot[-1][0]
    logger.debug(f"input->:{input}")
    for response, history in model.stream_chat(tokenizer,
                                               input,
                                               history,
                                               max_length=8192,
                                               top_p=0.8,
                                               temperature=1.0):
        chatbot[-1][1] = response
        yield chatbot, history

    logger.debug(f"history->:{history}")

def reset_user_input():
    return gr.update(value='')

def reset_state():
    return [], [], None

def add_text(history, text):
    history = history + [(text, None)]
    return history, gr.Textbox(value="", interactive=False)

with gr.Blocks(title = "智能客服小蓝", css="footer {visibility: hidden}") as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        bubble_full_width=False,
        height=800,
        show_copy_button = False,
        layout= "bubble",
        # avatar_images=((os.path.join(os.path.dirname(__file__), "../image/Einstein.jpg")), (os.path.join(os.path.dirname(__file__), "../image/openai.png")))
        avatar_images=("./image/Einstein.jpg", "./image/openai.png")
    )

    with gr.Row():
        with gr.Column(scale=9):
            user_input = gr.Textbox(show_label=False, placeholder="请输入您的问题,刷新页面可清除历史", lines=1, container=False)

        with gr.Column(min_width=1, scale=1):
            submitBtn = gr.Button("提交", variant="primary")

    begin = [{"role":"system", "content":"You are Intelligent Customer Service Blue, carefully analyzing the user's input and providing detailed and accurate answers.你是智能客服小蓝，仔细分析用户的输入，并作详细又准确的回答，记住使用中文回答问题。"}]
    history = gr.State(value=begin)

    subMsg = submitBtn.click(fn=add_text, inputs=[chatbot, user_input], outputs=[chatbot, user_input], queue=False).then(fn=predict, inputs=[chatbot, history], outputs=[chatbot, history], show_progress=True)
    inputMsg = user_input.submit(fn=add_text, inputs=[chatbot, user_input], outputs=[chatbot, user_input], queue=False).then(fn=predict, inputs=[chatbot, history], outputs=[chatbot, history], show_progress=True)

    subMsg.then(fn=lambda: gr.Textbox(interactive=True), inputs=None, outputs=[user_input], queue=False)
    inputMsg.then(fn=lambda: gr.Textbox(interactive=True), inputs=None, outputs=[user_input], queue=False)

auth=[(GradioUser, GradioPassword)]
demo.queue().launch(server_name={BindLocalIP}, server_port=int(BindPort), inbrowser=False, share=False, auth=auth)