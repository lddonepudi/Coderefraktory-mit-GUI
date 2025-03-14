import gradio as gr

def say_hello(name):
    return f"Hallo {name}!"

demo = gr.Interface(fn=say_hello, inputs="text", outputs="text")

if __name__ == "__main__":
    demo.launch()