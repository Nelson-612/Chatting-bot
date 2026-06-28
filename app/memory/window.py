from app.memory.base import MemoryStrategy
from app.models import Message


class WindowMemory(MemoryStrategy):
    """v2 -- keep only the most recent messages that fit the budget."""

    def build_context(
        self,
        messages: list[Message],
        budget_tokens: int,
        summary: str | None = None,
    ) -> list[dict]:
        kept_messages = []      # messages we keep
        total_tokens = 0        # running token total

        for message in reversed(messages):   # newest -> oldest
            # stop if this message would push us over budget
            if total_tokens + message.token_count > budget_tokens:
                break
            kept_messages.append(message)
            total_tokens += message.token_count

        # flip back to oldest -> newest, convert to role/content dicts
        return [
            {"role": message.role, "content": message.content}
            for message in reversed(kept_messages)
        ]
