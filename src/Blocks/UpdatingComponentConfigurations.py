
import platform
import gradio as gr

def change_textbox(choice):
    if choice == "short":
        return gr.Textbox(lines=2, visible=True)
    elif choice == "long":
        return gr.Textbox(lines=8, visible=True, value="Lorem ipsum dolor sit amet")
    else:
        return gr.Textbox(visible=False)


with gr.Blocks() as demo:
    radio = gr.Radio(
        ["short", "long", "none"], label="What kind of essay would you like to write?"
    )

    text = gr.Textbox(lines=2, interactive=True, show_copy_button=True)

    radio.change(fn=change_textbox, inputs=radio, outputs=text)


if platform.system() == 'Windows':
    demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
else:
    demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)
