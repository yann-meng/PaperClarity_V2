from skills.base import BaseSkill
from skills.shared import normalize_output, read_prompt


class ParagraphCloseReadingSkill(BaseSkill):
    name = "paragraph_close_reading"
    display_name = "段落精读"
    description = "逐句解释选中段落"
    supported_contexts = ["paragraph"]

    def build_prompt(self, context: dict, user_input: str | None = None) -> str:
        selected = "\n".join(x.get("text", "") for x in context.get("selected_blocks", []))
        template = read_prompt(__file__)
        return template.replace("{{selected_text}}", selected)

    def run(self, context: dict, llm_client, user_input: str | None = None) -> dict:
        return normalize_output(self.display_name, llm_client.generate_json(self.build_prompt(context, user_input)))
