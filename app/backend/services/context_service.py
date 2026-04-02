from models.document import Document


class ContextService:
    def build_paper_context(self, document: Document) -> dict:
        return {
            "title": document.title,
            "metadata": document.metadata,
            "section_titles": [s.title for s in document.sections],
            "content": "\n".join(b.text for b in document.blocks[:80]),
        }

    def build_section_context(self, document: Document, section_id: str) -> dict:
        section = next((s for s in document.sections if s.id == section_id), None)
        section_blocks = [b for b in document.blocks if b.section_id == section_id] if section else []
        return {
            "section": section.model_dump() if section else None,
            "blocks": [b.model_dump() for b in section_blocks],
        }

    def build_paragraph_context(self, document: Document, block_ids: list[str]) -> dict:
        indexes = [i for i, b in enumerate(document.blocks) if b.id in block_ids]
        selected, neighbors = [], []
        for idx in indexes:
            selected.append(document.blocks[idx])
            lo, hi = max(0, idx - 2), min(len(document.blocks), idx + 3)
            neighbors.extend(document.blocks[lo:hi])
        return {
            "selected_blocks": [b.model_dump() for b in selected],
            "neighbor_blocks": [b.model_dump() for b in neighbors],
        }

    def build_equation_context(self, document: Document, equation_id: str) -> dict:
        equation = next((e for e in document.equations if e.id == equation_id), None)
        if equation is None:
            return {}
        index = next((i for i, b in enumerate(document.blocks) if b.id == equation.block_id), 0)
        lo, hi = max(0, index - 2), min(len(document.blocks), index + 3)
        return {
            "equation": equation.model_dump(),
            "related_blocks": [b.model_dump() for b in document.blocks[lo:hi]],
        }

    def build_experiment_context(self, document: Document) -> dict:
        keywords = ["experiment", "results", "evaluation", "ablation"]
        candidates = [b for b in document.blocks if any(k in b.text.lower() for k in keywords)]
        if not candidates:
            candidates = document.blocks[-20:]
        return {
            "focus_blocks": [b.model_dump() for b in candidates[:40]],
        }
