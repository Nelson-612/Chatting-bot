from app.memory.base import MemoryStrategy
from app.models import Message


class BufferMemory(MemoryStrategy):
    """v1 -- send the entire history.

    Dead simple and correct until the conversation exceeds the model's context
    window, at which point the call fails. That failure is the whole reason the
    other strategies exist.
    """

    def build_context(
        self,
        messages: list[Message],
        budget_tokens: int,
        summary: str | None = None,
    ) -> list[dict]:
        return [{"role": m.role, "content": m.content} for m in messages]
