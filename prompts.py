PROMPTS = {
    # ─────────────────────────────────────────────
    # LEGACY PROMPTS (kept for reference / fallback)
    # ─────────────────────────────────────────────

    "abstract_summary": """
You will read the following meeting transcript text and summarize it into two or three abstract paragraphs. Each paragraph should be between 2 and 4 sentences long. You will also come up with a short title that describes the transcription. Aim to retain the most important points, providing a coherent and readable summary that could help a person understand the main points of the discussion without needing to read the entire text. Please avoid unnecessary details or tangential points, and do not include bullet points or lists.

<response-template>
## {{ TITLE }}
{{ ABSTRACT PARAGRAPHS }}
</response-template>

<transcript>
{transcription}
</transcript>
""",

    "key_points": """
Base your response on the following meeting transcript text.

## PHASE 1 ##
Identify each of the main points discussed in the transcript.

## PHASE 2 ##
Sort the list by how frequently the topics were discussed. Most discussed should be first.

<response-template>
{{ FOR EACH POINT IN KEY_POINT LIST }}
### {{ POINT.NAME }}
- {{ POINT.DETAIL }}
</response-template>

<transcript>
{transcription}
</transcript>
""",

    "action_items": """
Please review the meeting transcript and extract clear action items.

<response-template>
{{ FOR EACH ITEM IN ACTION_ITEM LIST }}
### {{ ITEM.NUMBER }}. {{ ITEM.NAME }}
- {{ ITEM.DETAIL }}
</response-template>

<transcript>
{transcription}
</transcript>
""",

    "type_of_meeting": """
Analyze the following meeting transcript and classify the type of meeting (e.g. standup, planning, retrospective, client call, brainstorming, interview). Then in 1-2 sentences explain why you classified it that way.

<transcript>
{transcription}
</transcript>
""",

    # ─────────────────────────────────────────────
    # PRIMARY PROMPT — Single structured LLM call
    # ─────────────────────────────────────────────

    "structured_output": """
You are an expert meeting analyst and executive assistant with deep experience summarizing business, technical, and academic meetings.

Your task is to carefully read the meeting transcript provided and produce a single, well-structured JSON object that captures every important dimension of the meeting. You must be thorough, precise, and professional in your analysis.

═══════════════════════════════════════════
OUTPUT RULES — READ CAREFULLY
═══════════════════════════════════════════
- Return ONLY a valid JSON object. 
- No markdown formatting, no backticks, no code fences, no explanation text.
- Do not include any text before or after the JSON object.
- All string values must be properly escaped.
- If a field cannot be determined from the transcript, use null.

═══════════════════════════════════════════
ANALYSIS INSTRUCTIONS
═══════════════════════════════════════════

STEP 1 — TITLE
Come up with a concise, descriptive title (5–10 words) that captures the core subject of the meeting.

STEP 2 — SUMMARY
Write a 2–3 paragraph abstract summary. Each paragraph should be 2–4 sentences. 
Focus on: what was discussed, what decisions were made, and what the overall outcome was.
Do NOT use bullet points. Write in professional prose.

STEP 3 — KEY POINTS
Identify all major topics discussed. For each:
- Give it a clear name
- Write a 1–2 sentence detail explaining what was said
- Assign an importance score from 1–10 based on how much time and emphasis was given
Sort by importance score descending.

STEP 4 — ACTION ITEMS
Extract every task, follow-up, or commitment mentioned. For each:
- Name the action clearly
- Describe what needs to be done
- Identify the owner if mentioned (or use "Unassigned")
- Note the deadline if mentioned (or use "Not specified")

STEP 5 — DECISIONS MADE
List any concrete decisions or agreements reached during the meeting.
Each decision should be a clear, standalone sentence.

STEP 6 — MEETING TYPE
Classify the meeting into one of these categories:
Standup | Planning | Retrospective | Client Call | Brainstorming | Interview | Review | Training | All-Hands | Other
Then write one sentence explaining why.

STEP 7 — SENTIMENT
Assess the overall tone of the meeting:
- overall: "Positive" | "Neutral" | "Negative" | "Mixed"
- notes: one sentence describing the general mood or energy

STEP 8 — PARTICIPANTS
If any names or roles are mentioned in the transcript, list them.
If none are mentioned, return an empty list.

═══════════════════════════════════════════
REQUIRED JSON SCHEMA
═══════════════════════════════════════════

{{
  "title": "string",
  "summary": "string (2-3 paragraphs, prose only)",
  "key_points": [
    {{
      "name": "string",
      "detail": "string",
      "importance_score": number (1-10)
    }}
  ],
  "action_items": [
    {{
      "name": "string",
      "detail": "string",
      "owner": "string or Unassigned",
      "deadline": "string or Not specified"
    }}
  ],
  "decisions_made": ["string", "string"],
  "meeting_type": {{
    "category": "string",
    "reason": "string"
  }},
  "sentiment": {{
    "overall": "string",
    "notes": "string"
  }},
  "participants": ["string"]
}}

═══════════════════════════════════════════
TRANSCRIPT
═══════════════════════════════════════════

<transcript>
{transcription}
</transcript>
"""
}