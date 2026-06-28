from app.memory.base import MemoryStrategy
from app.models import Message


class VectorMemory(MemoryStrategy):
    """v3 -- embed past turns, retrieve only the ones relevant to the new question.

    TODO(KaLong):
      - On write: embed each message, store the vector (sqlite-vss / faiss / pgvector
        / even a numpy cosine search to start -- keep it simple first).
      - On read: embed the latest user message, retrieve top-k similar past
        messages, send those + a small recent window within budget.
    This is the strategy that recalls a fact from 30 turns ago that a window
    would have dropped. Your eval harness is what proves that claim.
    """

    def build_context(
        self,
        messages: list[Message],
        budget_tokens: int,
        summary: str | None = None,
    ) -> list[dict]:
        raise NotImplementedError("KaLong writes this in v3")
