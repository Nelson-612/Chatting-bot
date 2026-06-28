from abc import ABC, abstractmethod

from app.models import Message


class MemoryStrategy(ABC):
    """A memory strategy decides WHICH messages actually get sent to the model.

    This single interface is the spine of the whole project. Every approach --
    buffer, window, summarization, vector retrieval -- is just a different
    implementation of build_context().

      input : the live (non-summarized) messages, a token budget, an optional
              running summary of older turns.
      output: the list of {"role", "content"} dicts to send to the LLM.

    NOTE for v2: summarization needs to *produce* a summary by calling the LLM.
    That's a separate concern from assembling context. When you get there you'll
    likely add an async `compact(...)` step that runs when a conversation goes
    over budget, writes the summary, and flips is_summarized=True on old rows.
    Revisit this interface then -- don't over-design it now.
    """

    @abstractmethod
    def build_context(
        self,
        messages: list[Message],
        budget_tokens: int,
        summary: str | None = None,
    ) -> list[dict]:
        ...
