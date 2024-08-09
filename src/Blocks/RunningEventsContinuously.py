
import math
import gradio as gr
import plotly.express as px
import numpy as np
import platform

plot_end = 2 * math.pi

def get_plot(period=1):
    global plot_end
    x = np.arange(plot_end - 2 * math.pi, plot_end, 0.02)
    y = np.sin(2*math.pi*period * x)
    fig = px.line(x=x, y=y)
    plot_end += 2 * math.pi
    if plot_end > 1000:
        plot_end = 2 * math.pi
    return fig

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            gr.Markdown("Change the value of the slider to automatically update the plot")
            period = gr.Slider(label="Period of plot", value=1, minimum=0, maximum=10, step=1)
            plot = gr.Plot(label="Plot (updates every half second)")

    dep = demo.load(fn=get_plot, inputs=None, outputs=plot, every=1)
    period.change(fn=get_plot, inputs=period, outputs=plot, every=1, cancels=[dep])

if __name__ == "__main__":
    demo.queue()
    if platform.system() == 'Windows':
        demo.launch(server_name="192.168.2.198", server_port=8001, inbrowser=False, share=False)
    else:
        demo.launch(server_name="192.168.2.200", server_port=8000, inbrowser=False, share=False)