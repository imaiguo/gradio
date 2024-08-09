import platform
import gradio as gr

shortcut_js = """
<script>
function shortcuts(e) {
    var event = document.all ? window.event : e;
    switch (e.target.tagName.toLowerCase()) {
        case "input":
        case "textarea":
        break;
        default:
        if (e.key.toLowerCase() == "s" && e.shiftKey) {
            document.getElementById("my_btn").click();
        }
    }
}

document.addEventListener('keypress', shortcuts, false);
</script>
"""

with gr.Blocks(head=shortcut_js) as demo:
    action_button = gr.Button(value="Name", elem_id="my_btn")
    textbox = gr.Textbox()
    action_button.click(lambda : "button pressed", None, textbox)
    

if platform.system() == 'Windows':
    demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
else:
    demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)