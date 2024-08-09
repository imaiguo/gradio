
import platform
import gradio as gr

def echo(text, request: gr.Request):
    if request:
        print("Request headers dictionary:", request.headers)
        print("IP address:", request.client.host)
        print("Query parameters:", dict(request.query_params))
    return text

io = gr.Interface(echo, "textbox", "textbox").launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)


if platform.system() == 'Windows':
    io = gr.Interface(echo, "textbox", "textbox").launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
else:
    io = gr.Interface(echo, "textbox", "textbox").launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)