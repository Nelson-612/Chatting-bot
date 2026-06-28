from app.memory.base import MemoryStrategy
from app.models import Message


class SummaryMemory(MemoryStrategy):
    """v2 -- running summary of old turns + a recent window of raw turns.

    The first genuinely non-trivial strategy. build_context() just assembles:
        [system summary] + [recent raw messages within budget]
    The hard part is the COMPACTION step that creates the summary -- that needs
    an LLM call, so it's async and lives outside build_context (see base.py note).

    TODO(KaLong):
      build_context():
        - If `summary` exists, prepend it as a system message
          (e.g. role="system", content="Summary so far: ...").
        - Then add the most recent raw messages that fit the remaining budget.
      compaction (design it; probably an async method or a service function):
        - Trigger when live tokens exceed some threshold of budget.
        - Take the oldest live messages, ask the LLM to fold them into the
          existing summary, save Conversation.summary, set is_summarized=True
          on those rows.
    """

    def build_context(
        self,
        messages: list[Message],
        budget_tokens: int,
        summary: str | None = None,
    ) -> list[dict]:
        raise NotImplementedError("KaLong writes this in v2")
