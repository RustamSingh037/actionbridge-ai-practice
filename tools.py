
import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).parent / "actionbridge_data"
DATA_DIR.mkdir(exist_ok=True)


def save_note(title: str, content: str) -> dict:
    """Save a note and verify it by reading it back."""
    safe_title = re.sub(r"[^a-zA-Z0-9_-]", "_", title).strip("_")
    safe_title = (safe_title or "note")[:60]
    path = DATA_DIR / f"{safe_title}.json"

    note = {"title": title, "content": content}
    path.write_text(
        json.dumps(note, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    saved = json.loads(path.read_text(encoding="utf-8"))

    if saved != note:
        raise RuntimeError("Verification failed.")

    return {
        "success": True,
        "message": "Note saved and verified!",
        "file": path.name,
        "verified": True,
    }


def list_notes() -> list:
    notes = []

    for path in sorted(DATA_DIR.glob("*.json")):
        try:
            notes.append(
                json.loads(path.read_text(encoding="utf-8"))
            )
        except (json.JSONDecodeError, OSError):
            continue

    return notes
