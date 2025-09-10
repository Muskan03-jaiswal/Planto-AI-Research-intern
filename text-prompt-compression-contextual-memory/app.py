import gradio as gr
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def compress_text(prompt):
    stop_words = ['the', 'a', 'an', 'is', 'are', 'was', 'were', 'and', 'or', 'but']
    compressed = ' '.join(word for word in prompt.split() if word.lower() not in stop_words)
    logger.debug(f"Compressed from '{prompt}' to '{compressed}'")
    return compressed

def process_input(text):
    if not text:
        return "Please enter some text to compress."
    compressed_text = compress_text(text)
    return f"Original: {text}\nCompressed: {compressed_text}"

with gr.Blocks(title="Text Prompt Compression Application") as iface:
    gr.Markdown("# Text Prompt Compression Application")
    gr.Markdown("Enter text to compress it by removing common stop words!")

    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(label="Enter Text", placeholder="Type here...")
            submit_btn = gr.Button("Compress", variant="primary")
        with gr.Column():
            output = gr.Textbox(label="Result", interactive=False)

    submit_btn.click(
        fn=process_input,
        inputs=text_input,
        outputs=output
    )

if __name__ == "__main__":
    iface.launch()