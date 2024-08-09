
import platform
import gradio as gr

blocks = gr.Blocks()

with blocks as demo:
    subject = gr.Textbox(placeholder="subject")
    verb = gr.Radio(["ate", "loved", "hated"])
    object = gr.Textbox(placeholder="object")

    with gr.Row():
        btn = gr.Button("Create sentence.")
        reverse_btn = gr.Button("Reverse sentence.")
        foo_bar_btn = gr.Button("Append foo")
        reverse_then_to_the_server_btn = gr.Button( "Reverse sentence and send to server.")

    def sentence_maker(w1, w2, w3):
        return f"{w1} {w2} {w3}"

    output1 = gr.Textbox(label="output 1")
    output2 = gr.Textbox(label="verb")
    output3 = gr.Textbox(label="verb reversed")
    output4 = gr.Textbox(label="front end process and then send to backend")

    btn.click(fn=sentence_maker, inputs=[subject, verb, object], outputs=output1)

    reverse_btn.click(
        fn=None, inputs=[subject, verb, object], outputs=output2, js="(s, v, o) => o + ' ' + v + ' ' + s"
    )

    verb.change(fn=lambda x: x, inputs=verb, outputs=output3, js="(x) => [...x].reverse().join('')")
    foo_bar_btn.click(fn=None, inputs=[], outputs=subject, js="(x) => x + ' foo'")

    reverse_then_to_the_server_btn.click(
        fn=sentence_maker,
        inputs=[subject, verb, object],
        outputs=output4,
        js="(s, v, o) => [s, v, o].map(x => [...x].reverse().join(''))",
    )

if platform.system() == 'Windows':
    demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
else:
    demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)