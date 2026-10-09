
import json
import ollama

MODEL = "llama3.1:8b"

SYSTEM_PROMPT = """
You are ActionBridge AI, a task-planning assistant.
Turn the user's request into a short, practical plan.

Return ONLY a JSON object with this exact structure:
{
  "task": "short task name",
  "steps": ["step one", "step two", "step three"]
}

Rules:
- Include 2 to 5 steps.
- The task must be a string.
- Steps must be a list of strings.
- Do not include markdown or extra text.
- Never claim that an action has been completed.
"""


def create_plan(user_request: str) -> dict:
    if not user_request.strip():
        raise ValueError("Please enter a task.")

    response = ollama.chat(
        model=MODEL,
        format="json",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_request},
        ],
    )

    result = json.loads(response["message"]["content"])

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
