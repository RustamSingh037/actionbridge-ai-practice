
import json
import streamlit as st
from google import genai

MODEL = "gemini-3.8-flash"

SYSTEM_PROMPT = """
You are ActionBridge AI, a task-planning assistant.
Turn the user's request into a short, practical plan.

Return ONLY a JSON object with this structure:
{
  "task": "short task name",
  "steps": ["step one", "step two", "step three"]
}

Rules:
- Include 2 to 5 steps.
- The task must be a string.
- Steps must be a list of strings.
- Do not include markdown or extra text.
- Never claim an action has been completed.
"""

def create_plan(user_request: str) -> dict:
    if not user_request.strip():
        raise ValueError("Please enter a task.")

    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. Add it in Streamlit Secrets."
        )

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=MODEL,
        contents=(
            f"{SYSTEM_PROMPT}\n\n"
            f"User request: {user_request}"
        ),
        config={
            "response_mime_type": "application/json",
        },
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    result = json.loads(response.text)

    if not isinstance(result.get("task"), str):
        raise ValueError("AI returned an invalid task.")

    steps = result.get("steps")
    if (
        not isinstance(steps, list)
        or not 2 <= len(steps) <= 5
        or not all(isinstance(step, str) for step in steps)
    ):
        raise ValueError("AI returned an invalid step list.")

    return result
