# 🎧 AI Meeting Summarizer

This project transforms audio recordings of meetings into concise, structured summaries with actionable items.

---

## 💡 Features

- Upload a meeting **audio** file (`.mp3`, `.wav`, etc.)
- Transcribe with **Faster-Whisper**
- Summarize with **OpenAI GPT-4.1** via LangChain
- Export summaries as **Markdown**, **JSON**, and **PDF**

---

## 🧠 AI Tools Used

- **OpenAI GPT-4.1**: for summarization, action extraction, and meeting classification.
- **Faster-Whisper**: for fast and accurate offline transcription.
- **LangChain**: to structure prompt chains.
- **Gradio**: to build an easy-to-use frontend.

---

## 🚧 Challenges Faced

- Managing long transcription times on CPU; resolved by using GPU with model optimization.
- Formatting structured outputs (headings, bullet lists) for PDF generation.
- Ensuring smooth UX while uploading large audio files.

---

## 🔧 If We Had More Time...

- Add **speaker diarization** for speaker labels
- Integrate with **Google Calendar** to auto-schedule follow-ups
- Add support for **multilingual transcription**
- Real time processing

---
