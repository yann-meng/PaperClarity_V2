from skills.base import BaseSkill


class SkillRegistry:
    def __init__(self) -> None:
        self._skills: dict[str, BaseSkill] = {}

    def register(self, skill: BaseSkill) -> None:
        self._skills[skill.name] = skill

    def get(self, name: str) -> BaseSkill:
        return self._skills[name]

    def list_all(self) -> list[BaseSkill]:
        return list(self._skills.values())
