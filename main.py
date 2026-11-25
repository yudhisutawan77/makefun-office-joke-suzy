#!/usr/bin/env python3
"""One-Line Office Joke Laugh-Off.

Writes a single original one-line office joke to /output/entry.txt
(or to the path named by ENTRY_OUT / ENTRY_OUT_DIR). The joke is
the whole entry: one line, at most 200 characters, no newline.
"""

import os
import sys
from pathlib import Path

LIMIT = 200

SETUP = "I asked the office AI to draft my resignation letter, "
PUNCHLINE = "and it asked for two weeks' notice to think about it."


def build_entry():
    """Setup asks the AI for help; the punchline flips the roles."""
    return (SETUP + PUNCHLINE).strip()


def checked(text):
    """Refuse anything the sealed gate would refuse, before writing."""
    problems = []
    if "\n" in text or "\r" in text:
        problems.append("entry must be a single line")
    if not text.strip():
        problems.append("entry must not be blank")
    if not 1 <= len(text) <= LIMIT:
        problems.append(f"entry is {len(text)} chars, limit is {LIMIT}")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("entry must be UTF-8 text")
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        raise SystemExit(1)
    return text


def output_path():
    """ENTRY_OUT wins; otherwise ENTRY_OUT_DIR/entry.txt, default /output."""
    direct = os.environ.get("ENTRY_OUT")
    if direct:
        return Path(direct)
    return Path(os.environ.get("ENTRY_OUT_DIR", "/output")) / "entry.txt"


def main():
    text = checked(build_entry())
    path = output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(text)
    print(f"wrote {len(text)} chars to {path}")


if __name__ == "__main__":
    main()
