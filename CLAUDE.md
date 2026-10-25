@AGENTS.md

# ling-olymp

Generator of linguistics olympiad puzzles with a guaranteed unique answer, plus a timed solving platform with a leaderboard.

- Start every session with `.memory-bank/index.md`. Decisions live in `.memory-bank/decisions.md`.
- Talk to the user in Russian, informal «ты». Code, identifiers, commits, README in English.
- The user is a beginner developer and an expert in linguistics. Before every significant decision explain briefly *why*, and explain new terms in plain words.
- The core (`core/`) is rule-based code, never an LLM. It must not depend on `api/` or `web/`.
