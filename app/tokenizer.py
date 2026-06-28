"""Count tokens once, at write time, and store the result on the Message row.

Uses tiktoken when available; otherwise falls back to a rough char-based estimate
so the project still runs without the dependency / without network access.
"""

try:
    import tiktoken

    _enc = tiktoken.get_encoding("cl100k_base")

    def count_tokens(text: str) -> int:
        return len(_enc.encode(text))

except Exception:  # tiktoken not installed

    def count_tokens(text: str) -> int:
        # ~4 characters per token is a decent rough estimate for English.
        return max(1, len(text) // 4)
