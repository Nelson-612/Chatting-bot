from app.memory.base import MemoryStrategy
from app.models import Message
from app.tokenizer import count_tokens


class SummaryMemory(MemoryStrategy):
    """v2 -- running summary of old turns + recent raw messages within budget."""

    def build_context(self, messages, budget_tokens, summary=None):
        context = []
        remaining = budget_tokens

        if summary:
            summary_text = "Summary of earlier conversation: " + summary
            context.append({"role": "system", "content": summary_text})
            remaining -= count_tokens(summary_text)

        kept = []
        total = 0
        for message in reversed(messages):
            if total + message.token_count > remaining:
                break
            kept.append(message)
            total += message.token_count

        for message in reversed(kept):
            context.append({"role": message.role, "content": message.content})

        return context
