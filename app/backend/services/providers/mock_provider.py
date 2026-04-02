
class MockProvider:
    def generate(self, prompt: str, system_prompt: str | None = None, temperature: float = 0.2) -> str:
        return f"[MOCK] {prompt[:200]}"

    def generate_json(self, prompt: str, system_prompt: str | None = None, temperature: float = 0.2) -> dict:
        return {
            "title": "Mock Result",
            "summary": "This is a mock LLM response.",
            "sections": [{"label": "Preview", "content": prompt[:300]}],
            "citations": [],
            "raw_text": f"[MOCK_JSON] {prompt[:200]}",
        }
