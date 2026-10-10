
import json
import streamlit as st
from groq import Groq

MODEL = "openai/gpt-oss-20b"

SYSTEM_PROMPT = """
You are ActionBridge AI, a task-planning assistant.
Return only a JSON object with this structure:
{
  "task": "short task name",
  "steps": ["step one", "step two", "step three"]
}
Rules:
- Include 2 to 5 practical steps.
- The task must be a string.
- Steps must be a list of strings.
- Never claim an action has been completed.
- Return JSON only, without markdown.
"""

def create_plan(user_request: str) -> dict:
    if not user_request.strip():
        raise ValueError("Please enter a task.")

    api_key = st.secrets.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Add it in Streamlit Secrets."
        )

    client = Groq(api_key=api_key, timeout=30.0, max_retries=2)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_request},
        ],
        temperature=0.2,
        max_completion_tokens=350,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    if not content:
        raise ValueError("The AI returned an empty response.")

    result = json.loads(content)
    if not isinstance(result.get("task"), str):
        raise ValueError("The AI returned an invalid task.")

    steps = result.get("steps")
    if (
        not isinstance(steps, list)
        or not 2 <= len(steps) <= 5
        or not all(isinstance(step, str) for step in steps)
    ):
        raise ValueError("The AI returned an invalid list of steps.")

    return result
