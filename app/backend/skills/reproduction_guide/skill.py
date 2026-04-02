from skills.base import BaseSkill
from skills.shared import normalize_output, read_prompt


class ReproductionGuideSkill(BaseSkill):
    name = "reproduction_guide"
    display_name = "复现指南"
    description = "生成可执行的复现路线"
    supported_contexts = ["paper"]

    def build_prompt(self, context: dict, user_input: str | None = None) -> str:
        template = read_prompt(__file__)
        return template.replace("{{paper_content}}", context.get("content", ""))

    def run(self, context: dict, llm_client, user_input: str | None = None) -> dict:
        return normalize_output(self.display_name, llm_client.generate_json(self.build_prompt(context, user_input)))
