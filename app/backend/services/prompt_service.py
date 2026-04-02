from pathlib import Path


class PromptService:
    def load_prompt(self, prompt_path: str) -> str:
        return Path(prompt_path).read_text(encoding="utf-8")

    def render(self, template: str, values: dict[str, str]) -> str:
        output = template
        for key, value in values.items():
            output = output.replace(f"{{{{{key}}}}}", value)
        return output
