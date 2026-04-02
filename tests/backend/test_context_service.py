from models.block import Block
from models.document import Document
from models.equation import Equation
from services.context_service import ContextService


def test_build_paragraph_context() -> None:
    blocks = [Block(id=f"b{i}", page=1, text=f"text {i}", order=i) for i in range(5)]
    doc = Document(id="d1", title="t", source_path="x.pdf", blocks=blocks)
    svc = ContextService()
    ctx = svc.build_paragraph_context(doc, ["b2"])
    assert len(ctx["selected_blocks"]) == 1
    assert len(ctx["neighbor_blocks"]) >= 3


def test_build_equation_context() -> None:
    blocks = [Block(id="b0", page=1, text="a", order=0), Block(id="b1", page=1, text="x=y", order=1)]
    eqs = [Equation(id="e1", page=1, raw_text="x=y", block_id="b1")]
    doc = Document(id="d1", title="t", source_path="x.pdf", blocks=blocks, equations=eqs)
    svc = ContextService()
    ctx = svc.build_equation_context(doc, "e1")
    assert ctx["equation"]["id"] == "e1"
