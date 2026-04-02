from skills.loader import load_skills
from skills.registry import SkillRegistry


def test_skill_auto_load() -> None:
    registry = SkillRegistry()
    load_skills(registry)
    names = {skill.name for skill in registry.list_all()}
    assert "paper_overview" in names
    assert "reproduction_guide" in names
