
# Gradio

## 1. 准备Python虚拟环境

```bash
> sudo apt install python3-venv python3-pip
> mkdir /opt/Data/PythonVenv
> cd /opt/Data/PythonVenv
> python3 -m venv gradio
> source /opt/Data/PythonVenv/gradio/bin/activate
```

## 2. 部署推理环境
```bash
> pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```


## 3. 启动服务

```bash
> python WebGradio/ChatInterfaceOpenAI.py
```
