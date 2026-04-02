import importlib
import pkgutil

from skills.base import BaseSkill
from skills.registry import SkillRegistry


def load_skills(registry: SkillRegistry) -> None:
    package = importlib.import_module("skills")
    for module_info in pkgutil.iter_modules(package.__path__):
        if module_info.name in {"base", "registry", "loader"}:
            continue
        module_name = f"skills.{module_info.name}.skill"
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            continue
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and issubclass(attr, BaseSkill) and attr is not BaseSkill:
                registry.register(attr())
