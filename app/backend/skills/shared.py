from pathlib import Path

PROMPT_FILE = "prompt.txt"


def read_prompt(current_file: str) -> str:
    return (Path(current_file).parent / PROMPT_FILE).read_text(encoding="utf-8")


def normalize_output(name: str, payload: dict) -> dict:
    return {
        "title": payload.get("title", name),
        "summary": payload.get("summary", ""),
        "sections": payload.get("sections", []),
        "citations": payload.get("citations", []),
        "raw_text": payload.get("raw_text", ""),
    }
