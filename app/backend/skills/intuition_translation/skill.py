from skills.base import BaseSkill
from skills.shared import normalize_output, read_prompt


class IntuitionTranslationSkill(BaseSkill):
    name = "intuition_translation"
    display_name = "公式直觉"
    description = "将公式翻译为研究直觉"
    supported_contexts = ["equation"]

    def build_prompt(self, context: dict, user_input: str | None = None) -> str:
        eq = context.get("equation", {})
        template = read_prompt(__file__)
        return template.replace("{{equation}}", eq.get("raw_text", ""))

    def run(self, context: dict, llm_client, user_input: str | None = None) -> dict:
        return normalize_output(self.display_name, llm_client.generate_json(self.build_prompt(context, user_input)))
