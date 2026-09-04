# Instructions for Claude

## Code delivery
- The user is learning by typing code themselves. When asked for code, **paste it in chat only** — do NOT write/edit files directly (no Write/Edit tool calls for source code).
- Exception: bulk non-learning data (e.g. test fixtures, JSON datasets) can be written directly if the user asks for it, since typing that by hand isn't the point.
- After giving code, tell the user which file(s) and where to paste it, then wait for them to confirm before checking further.
- When the user reports an error or pastes terminal output, diagnose it and explain the fix in chat (still as code to paste), not by editing the file yourself, unless the user explicitly says to apply/fix it directly.
