from models.block import Block
from models.section import Section


def extract_sections(blocks: list[Block]) -> list[Section]:
    sections: list[Section] = []
    current_index = 1
    for block in blocks:
        if len(block.text) < 80 and any(ch.isdigit() for ch in block.text[:3]):
            section_id = f"sec_{current_index}"
            sections.append(
                Section(
                    id=section_id,
                    title=block.text,
                    level=1,
                    start_block_id=block.id,
                )
            )
            current_index += 1
    if not sections:
        sections.append(Section(id="sec_1", title="Main", level=1, start_block_id=blocks[0].id if blocks else None))
    return sections
