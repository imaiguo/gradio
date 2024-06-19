
# Gradio 聊天会话窗口式界面

import os
import platform
import gradio as gr
import torch
from threading import Thread

from typing import Union
from pathlib import Path
from peft import AutoPeftModelForCausalLM, PeftModelForCausalLM
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizer,
    PreTrainedTokenizerFast,
    StoppingCriteria,
    StoppingCriteriaList,
    TextIteratorStreamer
)

ModelType = Union[PreTrainedModel, PeftModelForCausalLM]
TokenizerType = Union[PreTrainedTokenizer, PreTrainedTokenizerFast]

if platform.system() == "Windows":
    MODEL_PATH="E:/THUDM/chatglm3-6b"
else:
    MODEL_PATH="/opt/Data/ModelWeight/THUDM/chatglm3-6b"

def _resolve_path(path: Union[str, Path]) -> Path:
    return Path(path).expanduser().resolve()

def load_model_and_tokenizer(model_dir: Union[str, Path], trust_remote_code: bool = True) -> tuple[ModelType, TokenizerType]:
    model_dir = _resolve_path(model_dir)
    if (model_dir / 'adapter_config.json').exists():
        model = AutoPeftModelForCausalLM.from_pretrained(model_dir, trust_remote_code=trust_remote_code, device_map='cuda')
        tokenizer_dir = model.peft_config['default'].base_model_name_or_path
    else:
        print("--------load model--------")
        if platform.system() == "Windows":
            model = AutoModelForCausalLM.from_pretrained(model_dir, trust_remote_code=trust_remote_code, device_map='cuda').quantize(8)
        else:
            model = AutoModelForCausalLM.from_pretrained(model_dir, trust_remote_code=trust_remote_code, device_map='cuda')
        tokenizer_dir = model_dir

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_dir, trust_remote_code=trust_remote_code)
    return model, tokenizer

model, tokenizer = load_model_and_tokenizer(MODEL_PATH, trust_remote_code=True)

class StopOnTokens(StoppingCriteria):
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        stop_ids = [0, 2]
        for stop_id in stop_ids:
            if input_ids[0][-1] == stop_id:
                return True
        return False

def predict(history):
    print(f"history->{history}")
    stop = StopOnTokens()
    messages = []
    for idx, (user_msg, model_msg) in enumerate(history):
        if idx == len(history) - 1 and not model_msg:
            messages.append({"role": "user", "content": user_msg})
            break
        if user_msg:
            messages.append({"role": "user", "content": user_msg})
        if model_msg:
            messages.append({"role": "assistant", "content": model_msg})

    model_inputs = tokenizer.apply_chat_template(messages,
                                                 add_generation_prompt=False,
                                                 tokenize=True,
                                                 return_tensors="pt").to(next(model.parameters()).device)

    streamer = TextIteratorStreamer(tokenizer, timeout=60, skip_prompt=True, skip_special_tokens=True)

    generate_kwargs = {
        "input_ids": model_inputs,
        "streamer": streamer,
        "max_new_tokens": 8192,
        "do_sample": False,
        "top_p": 0.8,
        "temperature": 0.9,
        "stopping_criteria": StoppingCriteriaList([stop]),
        # "repetition_penalty": 0.8,
    }

    t = Thread(target=model.generate, kwargs=generate_kwargs)
    t.start()

    for new_token in streamer:
        if new_token != '':
            history[-1][1] += new_token
            yield history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        bubble_full_width=False,
        height=800,
        show_copy_button = False,
        layout= "bubble",
        avatar_images=((os.path.join(os.path.dirname(__file__), "../image/Einstein.jpg")), (os.path.join(os.path.dirname(__file__), "../image/openai.png")))
    )

    with gr.Row():
        with gr.Column(scale=9):
            user_input = gr.Textbox(show_label=False, placeholder="请输入您的问题,刷新页面可清除历史", lines=1, container=False)

        with gr.Column(min_width=2, scale=1):
            submitBtn = gr.Button("提交")

    def AddUserMessageToHistroy(query, history):
        return "", history + [[query, ""]]
    
    user_input.submit(AddUserMessageToHistroy, [user_input, chatbot], [user_input, chatbot], queue=False).then(predict, chatbot, chatbot)
    submitBtn.click(AddUserMessageToHistroy, [user_input, chatbot], [user_input, chatbot], queue=False).then(predict, chatbot, chatbot)

demo.queue()

if __name__ == "__main__":
    if platform.system() == 'Windows':
        demo.queue().launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
    else:
        demo.queue().launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)