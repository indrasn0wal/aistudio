import os
import json
import re
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import torch
from faster_whisper import WhisperModel
from prompts import PROMPTS
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT
import re

# Setup
load_dotenv()
os.environ['LANGCHAIN_VERBOSE'] = 'false'
device = "cuda" if torch.cuda.is_available() else "cpu"

# Whisper + LLM
f_model = WhisperModel("base", device=device, compute_type="int8")
llm = ChatOpenAI(temperature=0, model_name="gpt-4.1")

def generate_all_outputs(transcript):
    prompt = PromptTemplate.from_template(PROMPTS["structured_output"])
    chain = prompt | llm
    response = chain.invoke({"transcription": transcript}).content
    clean = re.sub(r"```json|```", "", response).strip()
    return json.loads(clean)

def export_to_markdown(data, file_path):
    lines = []

    lines.append(f"# {data['title']}")
    lines.append(f"## Summary\n{data['summary']}")

    kp = "\n".join(
        f"### {p['name']} *(importance: {p['importance_score']}/10)*\n- {p['detail']}"
        for p in data["key_points"]
    )
    lines.append(f"## Key Points\n{kp}")

    ai = "\n".join(
        f"### {i+1}. {item['name']}\n- {item['detail']}\n- **Owner:** {item['owner']}\n- **Deadline:** {item['deadline']}"
        for i, item in enumerate(data["action_items"])
    )
    lines.append(f"## Action Items\n{ai}")

    if data.get("decisions_made"):
        decisions = "\n".join(f"- {d}" for d in data["decisions_made"])
        lines.append(f"## Decisions Made\n{decisions}")

    lines.append(f"## Meeting Type\n**{data['meeting_type']['category']}** — {data['meeting_type']['reason']}")
    lines.append(f"## Sentiment\n**{data['sentiment']['overall']}** — {data['sentiment']['notes']}")

    if data.get("participants"):
        participants = "\n".join(f"- {p}" for p in data["participants"])
        lines.append(f"## Participants\n{participants}")

    md_content = "\n\n".join(lines)
    Path(file_path).write_text(md_content)
    return md_content

def export_to_json(data, file_path):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

def export_to_pdf(markdown_text, output_pdf_path):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm
    )

    styles = getSampleStyleSheet()

    h1 = ParagraphStyle('H1', fontSize=18, fontName='Helvetica-Bold', spaceAfter=6, spaceBefore=4)
    h2 = ParagraphStyle('H2', fontSize=14, fontName='Helvetica-Bold', spaceAfter=4, spaceBefore=10)
    h3 = ParagraphStyle('H3', fontSize=11, fontName='Helvetica-Bold', spaceAfter=2, spaceBefore=6)
    body = ParagraphStyle('Body', fontSize=10, fontName='Helvetica', spaceAfter=3, leading=14)
    bullet = ParagraphStyle('Bullet', fontSize=10, fontName='Helvetica', leftIndent=15, spaceAfter=2, leading=13)

    def sanitize(text):
        # escape reportlab special chars
        text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        # convert **bold** to <b>bold</b>
        text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
        # remove remaining * markers
        text = re.sub(r"\*(importance:.*?)\*", r"(\1)", text)
        text = text.replace("→", "->").replace("•", "-")
        return text

    story = []

    for line in markdown_text.split("\n"):
        stripped = line.strip()

        if not stripped:
            story.append(Spacer(1, 4))
            continue

        try:
            # H1
            if stripped.startswith("# ") and not stripped.startswith("## "):
                text = sanitize(stripped[2:].strip())
                story.append(Paragraph(text, h1))

            # H2
            elif stripped.startswith("## "):
                text = sanitize(stripped[3:].strip())
                story.append(Paragraph(text, h2))

            # H3
            elif stripped.startswith("### "):
                text = sanitize(stripped[4:].strip())
                story.append(Paragraph(text, h3))

            # Bullet - or *
            elif re.match(r"^[-*] ", stripped):
                text = sanitize(stripped[2:].strip())
                story.append(Paragraph(f"• {text}", bullet))

            # Numbered list
            elif re.match(r"^\d+\.", stripped):
                text = sanitize(stripped)
                story.append(Paragraph(text, h3))

            # Normal text
            else:
                text = sanitize(stripped)
                story.append(Paragraph(text, body))

        except Exception:
            continue

    doc.build(story)

def process_audio(audio_path):
    if audio_path is None:
        return "Please upload an audio file.", None, None, None

    segments, _ = f_model.transcribe(audio_path)
    segments = list(segments)
    transcript = "\n".join([
        f"[{seg.start:.1f}s → {seg.end:.1f}s] {seg.text.strip()}"
        for seg in segments
    ])

    try:
        results = generate_all_outputs(transcript)
    except json.JSONDecodeError:
        return "Error: AI returned malformed output. Please try again.", None, None, None

    os.makedirs("outputs", exist_ok=True)
    md_path = "outputs/summary.md"
    json_path = "outputs/summary.json"
    pdf_path = "outputs/summary.pdf"

    md_text = export_to_markdown(results, md_path)
    export_to_json(results, json_path)
    export_to_pdf(md_text, pdf_path)

    return md_text, md_path, json_path, pdf_path