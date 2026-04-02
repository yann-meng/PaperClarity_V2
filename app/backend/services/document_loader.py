from pathlib import Path


def detect_doc_type(file_path: str) -> str:
    suffix = Path(file_path).suffix.lower()
    if suffix == ".pdf":
        return "pdf"
    raise ValueError(f"Unsupported file type: {suffix}")
