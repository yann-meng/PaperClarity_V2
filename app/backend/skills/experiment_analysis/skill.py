from skills.base import BaseSkill
from skills.shared import normalize_output, read_prompt


class ExperimentAnalysisSkill(BaseSkill):
    name = "experiment_analysis"
    display_name = "实验分析"
    description = "分析实验设计与结果"
    supported_contexts = ["paper", "section"]

    def build_prompt(self, context: dict, user_input: str | None = None) -> str:
        text = "\n".join(x.get("text", "") for x in context.get("focus_blocks", []))
        template = read_prompt(__file__)
        return template.replace("{{experiment_content}}", text)

    def run(self, context: dict, llm_client, user_input: str | None = None) -> dict:
        return normalize_output(self.display_name, llm_client.generate_json(self.build_prompt(context, user_input)))
