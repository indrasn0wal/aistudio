PROMPTS = {
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
Analyze and tell the type of the meeting. 

<transcript>
{transcription}
</transcript>
"""
}
