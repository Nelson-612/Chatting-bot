from app.memory.base import MemoryStrategy
from app.models import Message


class WindowMemory(MemoryStrategy):
    """v2 -- keep only the most recent messages that fit the budget.

    TODO(KaLong):
      - Walk messages NEWEST -> OLDEST, accumulating token_count.
      - Stop before adding a message would exceed budget_tokens.
      - Return the kept messages in CHRONOLOGICAL order (oldest -> newest).

    Think about:
      - A single message larger than the entire budget (don't infinite-loop / don't
        return empty silently -- decide and document the behavior).
      - Whether you keep a leading system message regardless of the window.
      - Cheap because no LLM call; the cost is it simply forgets old facts.
        Your eval harness should *show* that forgetting.
    """

    def build_context(
        self,
        messages: list[Message],
        budget_tokens: int,
        summary: str | None = None,
    ) -> list[dict]:
        raise NotImplementedError("KaLong writes this in v2")
