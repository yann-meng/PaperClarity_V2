from datetime import datetime

from models.note import Note


class ExportService:
    def notes_to_markdown(self, document_title: str, notes: list[Note]) -> str:
        lines = [f"# {document_title}", "", f"导出时间: {datetime.utcnow().isoformat()} UTC", ""]
        for note in notes:
            lines.append(f"## {note.title}")
            lines.append("")
            lines.append(note.content)
            lines.append("")
            if note.citations:
                lines.append("引用:")
                for c in note.citations:
                    lines.append(f"- page={c.get('page')} block_id={c.get('block_id')}")
                lines.append("")
        return "\n".join(lines)
