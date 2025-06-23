import gradio as gr
from summarizer import process_audio

with gr.Blocks(title="Meeting Summarizer") as app:
    gr.Markdown("## Upload a Meeting Audio File")
    gr.Markdown("It will be transcribed, summarized, and exported in Markdown, JSON, and PDF.")

    with gr.Row():
        audio_input = gr.Audio(type="filepath", label="Upload Audio File")
        generate_btn = gr.Button("Transcribe")

    md_display = gr.Markdown(label="Summary Preview")
    file_md = gr.File(label="📄 Download .md")
    file_json = gr.File(label="🧾 Download .json")
    file_pdf = gr.File(label="📘 Download .pdf")

    generate_btn.click(
        fn=process_audio,
        inputs=[audio_input],
        outputs=[md_display, file_md, file_json, file_pdf]
    )

app.launch(share=True, debug=True)
