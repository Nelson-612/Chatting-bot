"""v3 -- evaluation harness. This is where your HONEST resume number comes from.

Goal: prove one memory strategy beats another with numbers YOU computed and can
defend on a whiteboard.

Design (TODO(KaLong)):
  - Define test scripts: multi-turn conversations where a LATER turn depends on a
    fact stated in an EARLIER turn. Example:
        turn 1  (user): "My name is KaLong and I live in San Jose."
        ...     filler turns to push that fact past a small window...
        turn N  (user): "What's my name and where do I live?"
      expected_substrings = ["KaLong", "San Jose"]
  - For each strategy (buffer, window, summary, vector):
        run each script through the real chat flow,
        check whether the final answer contains expected_substrings -> recalled?
        record tokens sent per turn and latency.
  - Aggregate per strategy: recall rate, avg tokens/turn, avg latency.
  - Print a comparison table. THAT table backs your bullet, e.g.
    "cut tokens/turn ~X% via summarization while holding recall at Y% on a
     Z-script eval set."

Tip: debug the harness plumbing offline with EchoProvider first (it can't recall
facts, so expect ~0% recall -- that confirms the harness measures correctly),
then point it at a real model.
"""


def main():
    raise NotImplementedError("KaLong builds the harness in v3")


if __name__ == "__main__":
    main()
