from abc import ABC, abstractmethod

from app.config import settings


class LLMProvider(ABC):
    """Abstracts the model so the actual choice is made at build time, not baked in."""

    @abstractmethod
    async def chat(self, messages: list[dict]) -> str:
        ...


class EchoProvider(LLMProvider):
    """Offline/dev provider -- NO network, NO API key.

    Lets you test auth, persistence, and the whole memory-wiring end to end
    without spending a cent or needing connectivity. Swap to OpenAIProvider
    when you want real answers.
    """

    async def chat(self, messages: list[dict]) -> str:
        last_user = next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"), ""
        )
        return f"[echo] received {len(messages)} msgs. Last user said: {last_user!r}"


class OpenAIProvider(LLMProvider):
    """Real provider. Requires `openai` installed and OPENAI_API_KEY set."""

    def __init__(self) -> None:
        from openai import AsyncOpenAI

        self._client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def chat(self, messages: list[dict]) -> str:
        resp = await self._client.chat.completions.create(
            model=settings.model_name,
            messages=messages,
        )
        return resp.choices[0].message.content or ""


def get_provider() -> LLMProvider:
    if settings.llm_provider == "openai" and settings.openai_api_key:
        return OpenAIProvider()
    return EchoProvider()
