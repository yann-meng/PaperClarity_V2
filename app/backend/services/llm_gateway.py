import logging
import time

from core.config import settings
from services.providers.mock_provider import MockProvider
from services.providers.openai_compatible import OpenAICompatibleProvider

logger = logging.getLogger(__name__)


class LLMGateway:
    def __init__(self) -> None:
        if settings.llm_provider == "openai_compatible":
            self.provider = OpenAICompatibleProvider(
                base_url=settings.llm_base_url,
                api_key=settings.llm_api_key,
                model=settings.llm_model,
                timeout_seconds=settings.llm_timeout_seconds,
            )
        else:
            self.provider = MockProvider()

    def generate(self, prompt: str, system_prompt: str | None = None, temperature: float = 0.2) -> str:
        last_error: Exception | None = None
        for attempt in range(2):
            try:
                return self.provider.generate(prompt, system_prompt, temperature)
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                logger.warning("LLM generate failed at attempt %s: %s", attempt + 1, exc)
                time.sleep(0.5)
        raise RuntimeError(f"LLM generation failed: {last_error}")

    def generate_json(self, prompt: str, system_prompt: str | None = None, temperature: float = 0.2) -> dict:
        last_error: Exception | None = None
        for attempt in range(2):
            try:
                return self.provider.generate_json(prompt, system_prompt, temperature)
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                logger.warning("LLM generate_json failed at attempt %s: %s", attempt + 1, exc)
                time.sleep(0.5)
        raise RuntimeError(f"LLM JSON generation failed: {last_error}")
