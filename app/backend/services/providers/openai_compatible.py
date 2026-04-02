import httpx


class OpenAICompatibleProvider:
    def __init__(self, base_url: str, api_key: str, model: str, timeout_seconds: int = 30):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.timeout_seconds = timeout_seconds

    def generate(self, prompt: str, system_prompt: str | None = None, temperature: float = 0.2) -> str:
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        with httpx.Client(timeout=self.timeout_seconds) as client:
            res = client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
            res.raise_for_status()
            data = res.json()
        return data["choices"][0]["message"]["content"]

    def generate_json(self, prompt: str, system_prompt: str | None = None, temperature: float = 0.2) -> dict:
        content = self.generate(prompt=prompt, system_prompt=system_prompt, temperature=temperature)
        return {"raw_text": content}
