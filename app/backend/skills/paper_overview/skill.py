from skills.base import BaseSkill
from skills.shared import normalize_output, read_prompt


class PaperOverviewSkill(BaseSkill):
    name = "paper_overview"
    display_name = "整篇总览"
    description = "理解整篇论文并输出结构化总结"
    supported_contexts = ["paper"]

    def build_prompt(self, context: dict, user_input: str | None = None) -> str:
        template = read_prompt(__file__)
        return template.replace("{{paper_content}}", context.get("content", ""))

    def run(self, context: dict, llm_client, user_input: str | None = None) -> dict:
        prompt = self.build_prompt(context, user_input)
        return normalize_output(self.display_name, llm_client.generate_json(prompt))
