import os
import json
from pathlib import Path
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from markdown2 import markdown
import pdfkit
import torch
from faster_whisper import WhisperModel
from prompts import PROMPTS

# Setup
os.environ['LANGCHAIN_VERBOSE'] = 'false'
device = "cuda" if torch.cuda.is_available() else "cpu"

# Whisper + LLM
f_model = WhisperModel("base", device=device, compute_type="int8")
llm = ChatOpenAI(temperature=0, model_name="gpt-4.1")

def run_prompt(prompt_name, transcript):
    prompt_text = PROMPTS[prompt_name].replace("{transcription}", transcript)
    chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template(prompt_text))
    return chain.run({})

def generate_all_outputs(transcript):
    return {
        "title_and_abstract": run_prompt("abstract_summary", transcript),
        "key_points": run_prompt("key_points", transcript),
        "action_items": run_prompt("action_items", transcript),
        "type_of_meeting": run_prompt("type_of_meeting", transcript)
    }

def export_to_markdown(data, file_path):
    lines = [
        data["title_and_abstract"],
        "## Key Points\n" + data["key_points"],
        "## Action Items\n" + data["action_items"],
        "## Type of Meeting\n" + data["type_of_meeting"]
    ]
    md_content = "\n\n".join(lines)
    Path(file_path).write_text(md_content)
    return md_content

def export_to_json(data, file_path):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

def export_to_pdf(markdown_text, output_pdf_path):
    html_text = markdown(markdown_text)
    pdfkit.from_string(html_text, output_pdf_path)

def process_audio(audio_path):
    if audio_path is None:
        return "Please upload an audio file.", None, None, None

    segments, _ = f_model.transcribe(audio_path)
    transcript = " ".join([seg.text for seg in segments])

    results = generate_all_outputs(transcript)

    os.makedirs("outputs", exist_ok=True)
    md_path = "outputs/summary.md"
    json_path = "outputs/summary.json"
    pdf_path = "outputs/summary.pdf"

    md_text = export_to_markdown(results, md_path)
    export_to_json(results, json_path)
    export_to_pdf(md_text, pdf_path)

    return md_text, md_path, json_path, pdf_path
