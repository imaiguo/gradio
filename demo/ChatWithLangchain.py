
# Gradio 聊天会话窗口式界面

import time
import os
import platform
import gradio as gr

from typing import Optional, List, Any
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms.base import LLM
from transformers import AutoTokenizer, AutoModel

if platform.system() == "Windows":
    MODEL_PATH="E:/THUDM/chatglm3-6b"
else:
    MODEL_PATH="/opt/Data/THUDM/chatglm3-6b"

class ChatGLM(LLM):
    tokenizer: AutoTokenizer = None
    model: AutoModel = None

    @property
    def _llm_type(self) -> str:
        return "ChatGLM3"

    def load_model(self, model_dir):
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(model_dir, trust_remote_code=True, device="cuda").eval()

    def _call(
            self,
            prompt: str,
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        response, history = self.model.chat(self.tokenizer, prompt, history=[])

        return response

def load_documents(directory="documents"):
    """
    使用langchain框架加载documents下的文件，并进行拆分, 关于对应文件的切分处理仍需要进行改进
    :param directory:
    :return:
    """
    documents = []
    if not os.path.exists(directory):
        os.mkdir(directory)
    # 获取该目录下所有文件名
    files = os.listdir(directory)
    for file in files:
        # 根据文件夹类型的不同, 分别调用langchain框架中对应方法加载文件
        print(f"当前正在加载的文件是{file}")
        # 获取绝对路径
        file_path = os.path.abspath(os.path.join(directory, file))
        if file.endswith('.txt'):
            loader = DirectoryLoader(directory)
            document = loader.load()
            documents.extend(document)                  # 使用extend方法将document元素逐个添加到documents中
        elif file.endswith('.docx'):
            # UnstructuredWordDocumentLoader模块需要绝对路径
            loader = UnstructuredWordDocumentLoader(file_path)
            document = loader.load()
            documents.extend(document)
        elif file.endswith('.pdf'):
            # PyPDFLoader需要绝对路径
            loader = PyPDFLoader(file_path)
            document = loader.load()
            documents.extend(document)
        else:
            print(f"当前文件 '{file}' 的类型无法处理，请检查文件类型是否正确")
    # 文档拆分: 按照字符来分割文本
    # 创建分割器
    text_spliter = CharacterTextSplitter(chunk_size=256, chunk_overlap=0)
    # 分割文档
    split_docs = text_spliter.split_documents(documents)

    return split_docs

embedding_model_dict = {"text2vec3": "/opt/Data/ModelWeight/shibing624/text2vec-base-chinese"}

def load_embedding_model(model_name):
    encode_kwargs = {"normalize_embeddings": False}
    model_kwargs = {"device": "cuda:0"}
    return HuggingFaceEmbeddings(
        model_name=embedding_model_dict[model_name],
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

def store_chroma(docs, embeddings, persist_directory="VectorStore"):
    db = Chroma.from_documents(docs, embeddings, persist_directory=persist_directory)
    db.persist()

    return db

embeddings = load_embedding_model('text2vec3')

if not os.path.exists('VectorStore'):
    os.mkdir("VectorStore")
    documents = load_documents()
    db = store_chroma(documents, embeddings)
else:
    db = Chroma(persist_directory='VectorStore', embedding_function=embeddings)

llm = ChatGLM()
llm.load_model(MODEL_PATH)

# 创建qa
QA_CHAIN_PROMPT = PromptTemplate.from_template("""你是智能客服小e，仔细分析用户的输入，并作详细又准确的回答，{context},问题: {question}""")
retriever = db.as_retriever()

qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    verbose=True,
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)

def add_text(history, text):
    if history is None:
        history = []
    history = history + [(text, None)]

    return history, gr.update(value="", interactive=False)

def add_file(history, file):
    global qa
    directory = os.path.dirname(file.name)
    documents = load_documents(directory)
    db = store_chroma(documents, embeddings)
    retriever = db.as_retriever()
    qa.retriever = retriever
    history = history + [((file.name,), None)]

    return history

def bot(history):
    message = history[-1][0]
    response = qa({"query": message})['result']
    history[-1][1] = ""

    for character in response:
        history[-1][1] += character
        time.sleep(0.05)
        yield history

with gr.Blocks(css="footer {visibility: hidden}", title = "LLM能力演示") as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="AI Bot",
        height=800,
        bubble_full_width=False,
        avatar_images=((os.path.join(os.path.dirname(__file__), "../image/Einstein.jpg")), (os.path.join(os.path.dirname(__file__), "../image/openai.png")))
    )

    with gr.Row():
        user_input = gr.Textbox(
            scale=9,
            show_label=False,
            placeholder="Enter text and press enter, or upload an image",
            container=False,
        )

        with gr.Column(min_width=2, scale=1):
            submitBtn = gr.Button("提交")

    txt_msg = user_input.submit(add_text, [chatbot, user_input], [chatbot, user_input], queue=False).then(bot, chatbot, chatbot)
    txt_msg.then(lambda: gr.update(interactive=True), None, [user_input], queue=False)

    submitBtn.click(add_text, [chatbot, user_input], [chatbot, user_input], queue=False).then(bot, chatbot, chatbot)

if __name__ == "__main__":
    demo.queue()
    demo.launch(server_name='192.168.2.200', server_port=8000, share=False)
