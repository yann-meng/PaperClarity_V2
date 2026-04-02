from abc import ABC, abstractmethod
from typing import Any


class BaseSkill(ABC):
    name: str = "base"
    display_name: str = "Base Skill"
    description: str = ""
    supported_contexts: list[str] = []

    @abstractmethod
    def build_prompt(self, context: dict[str, Any], user_input: str | None = None) -> str:
        ...

    @abstractmethod
    def run(self, context: dict[str, Any], llm_client: Any, user_input: str | None = None) -> dict[str, Any]:
        ...

    def output_schema(self) -> dict[str, Any]:
        return {
            "title": "string",
            "summary": "string",
            "sections": [{"label": "string", "content": "string"}],
            "citations": [{"page": 1, "block_id": "b_1_1"}],
            "raw_text": "string",
        }
