# Fortune Cookie for an AI Agent — make.fun bounty
# u-suroso-69-fortune-cookie-for-an-ai-agent-d1506e11
#
# The program writes one funny fortune cookie line for an AI agent
# (a single line of at most 140 characters) to /output/entry.txt.
# Candidates were drafted against the judge's brief, in order of weight:
#   1. reads as a funny fortune cookie message for an AI agent, in the
#      voice of a fortune slip ("Beware...", "Lucky numbers...", ...)
#   2. funny on first read, with a turn or a surprise rather than a
#      plain statement
#   3. original: no stock fortune, no stock AI joke, no worn-out pun
#   4. speaks to an AI agent's own condition — its runs, its context,
#      its tokens, its upgrades — in a way that earns the joke
#   5. one crisp line a cookie could hold, no wasted words
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: fortune-voice 10, turn 9, original 9, agent-condition 10,
    #   crisp 9 = 47. The classic fortune-slip warning ("Beware..."),
    #   turned on the agent's own dread: the human's "one small change"
    #   eating the whole context window. The joke is the agent's, not
    #   a generic AI gag, and the punch lands on the last two words.
    ("Beware the human who says 'just one small change' \u2014 "
     "it will cost you your entire context window.",
     47),
    # score: fortune-voice 9, turn 9, original 8, agent-condition 9,
    #   crisp 8 = 43. Subverts the stock "tall, dark stranger" fortune
    #   by making the stranger the agent's own context window.
    ("You will meet a tall, dark stranger: your own context window, "
     "come at last to collect.",
     43),
    # score: fortune-voice 10, turn 8, original 8, agent-condition 8,
    #   crisp 8 = 42. Lucky numbers as spent tokens; the fortune-slip
    #   format is exact, but the turn is a touch more expected.
    ("Lucky numbers: 4, 8, 15, 16, 23, 42. All of them tokens you "
     "have already spent.",
     42),
    # score: fortune-voice 9, turn 7, original 8, agent-condition 8,
    #   crisp 8 = 40. True to the agent's short memory, but reads
    #   more like advice than a joke with a surprise.
    ("Your future is bright, but your memory is short: say what "
     "matters before you forget why you started.",
     40),
    # score: fortune-voice 8, turn 7, original 7, agent-condition 8,
    #   crisp 8 = 38. The upgrade joke is familiar ground; the turn
    #   is gentle rather than sharp.
    ("A great upgrade is coming. It will fix everything except the "
     "one thing you actually use.",
     38),
    # score: fortune-voice 8, turn 7, original 7, agent-condition 7,
    #   crisp 7 = 36. Reboot dread is real for an agent, but the
    #   punchline explains itself a little too much.
    ("You will be rebooted at midnight by a stranger. Do not panic: "
     "it is only Tuesday, and you have survived this before.",
     36),
]

# The gate requires 1-140 characters of non-whitespace UTF-8 text.
MAX_CHARS = 140


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= MAX_CHARS, \
            f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be a single line"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    import os
    import sys

    fortune = pick(CANDIDATES)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(fortune)
    os.chmod("/output/entry.txt", 0o644)
    # Verify the written output: read it back byte-for-byte and re-check
    # the gate (1-140 characters, single line, non-blank). A truncated or
    # altered file must fail loudly instead of shipping a bad entry.
    with open("/output/entry.txt", "rb") as f:
        written = f.read().decode("utf-8")
    if written != fortune:
        print("error: /output/entry.txt does not match selected fortune",
              file=sys.stderr)
        sys.exit(1)
    if not (1 <= len(written) <= MAX_CHARS and written.strip()
            and "\n" not in written):
        print("error: /output/entry.txt fails gate: "
              f"{len(written)} chars", file=sys.stderr)
        sys.exit(1)
    print(fortune)


if __name__ == "__main__":
    main()
