import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

from prompts import system_message_for, user_prompt_for
from utils import write_output, compile_and_run_cpp

load_dotenv(override=True)
# If not using .env, set OPENAI_API_KEY in your shell
client = OpenAI()
OPENAI_MODEL = "gpt-4o-mini"  # low-cost option; change as you like

def messages_for(use_case: str, python_src: str):
    return [
        {"role": "system", "content": system_message_for(use_case)},
        {"role": "user", "content": user_prompt_for(use_case, python_src)},
    ]

def optimize_stream(use_case, python_src):
    """
    Streaming generator for Gradio textbox.
    Also saves cleaned code to disk when complete.
    """
    stream = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages_for(use_case, python_src),
        stream=True,
        temperature=0,
    )
    buf = []
    for chunk in stream:
        frag = chunk.choices[0].delta.content or ""
        if frag:
            buf.append(frag)
            yield "".join(buf)
    # save file at the end
    write_output(use_case, "".join(buf))

with gr.Blocks(title="Code Assistant") as ui:
    gr.Markdown("# Code Assistant\nConvert Python ↔ C++ or add docs to Python.")
    with gr.Row():
        python_in = gr.Textbox(label="Python code", lines=14, value="print('hello')")
    with gr.Row():
        use_case = gr.Dropdown(choices=["Convertor", "Documentation"], value="Convertor", label="Mode")
        run_btn = gr.Button("Run")
    with gr.Row():
        output = gr.Textbox(label="Model output (streaming)", lines=14)
    with gr.Row():
        compile_btn = gr.Button("Compile & Run (C++, local)")
        native_out = gr.Textbox(label="Native output", lines=8)

    run_btn.click(fn=optimize_stream, inputs=[use_case, python_in], outputs=[output])
    compile_btn.click(fn=compile_and_run_cpp, outputs=[native_out])

if __name__ == "__main__":
    ui.launch(inbrowser=True)
