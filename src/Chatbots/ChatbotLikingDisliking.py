
import platform
import gradio as gr

def greet(history, input):
    return history + [(input, "Hello, " + input)]

def vote(data: gr.LikeData):
    if data.liked:
        print("You upvoted this response: " + data.value)
    else:
        print("You downvoted this response: " + data.value)
    

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(height=700, bubble_full_width=False)
    textbox = gr.Textbox()
    textbox.submit(fn=greet, inputs=[chatbot, textbox], outputs=[chatbot])
    chatbot.like(fn=vote, inputs=None, outputs=None)  # Adding this line causes the like/dislike icons to appear in your chatbot
    
if __name__ == "__main__":
    if platform.system() == 'Windows':
        demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
    else:
        demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)