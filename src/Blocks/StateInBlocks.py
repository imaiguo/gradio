
# 1. We store the used letters in used_letters_var. In the constructor of State, we set the initial value of this to [], an empty list.
# 2. In btn.click(), we have a reference to used_letters_var in both the inputs and outputs.
# 3. In guess_letter, we pass the value of this State to used_letters, and then return an updated value of this State in the return statement.

import platform
import gradio as gr

secret_word = "gradio"

with gr.Blocks() as demo:
    used_letters_var = gr.State([])
    with gr.Row() as row:
        with gr.Column():
            input_letter = gr.Textbox(label="Enter letter")
            btn = gr.Button("Guess Letter")
        with gr.Column():
            hangman = gr.Textbox(
                label="Hangman",
                value="_"*len(secret_word)
            )
            used_letters_box = gr.Textbox(label="Used Letters")

    def guess_letter(letter, used_letters):
        print(f"input_letter->{letter}")
        print(f"used_letters->{used_letters}")
        used_letters.append(letter)
        answer = "".join([(letter if letter in used_letters else "_") for letter in secret_word])

        return {
            used_letters_var: used_letters,
            used_letters_box: ", ".join(used_letters),
            hangman: answer
        }

    btn.click(fn=guess_letter, inputs=[input_letter, used_letters_var], outputs=[used_letters_var, used_letters_box, hangman])

if __name__ == "__main__":
    if platform.system() == 'Windows':
        demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
    else:
        demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)