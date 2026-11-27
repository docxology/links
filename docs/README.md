# Documentation

This directory contains comprehensive documentation for the links analysis pipeline.

## Reading Order

1. [`USER_GUIDE.md`](USER_GUIDE.md) — how to run and what the outputs mean.
2. [`ARCHITECTURE.md`](ARCHITECTURE.md) — data flow, stages, and design decisions.
3. [`API_REFERENCE.md`](API_REFERENCE.md) — module functions, CLI flags, data shapes.
4. [`TESTING.md`](TESTING.md) — how to test, markers, and coverage.
5. [`DEVELOPMENT.md`](DEVELOPMENT.md) — workflow, `uv`, contributing.
6. [`SUMMARY.md`](SUMMARY.md) — quick overview and code map.
7. [`CHANGELOG.md`](CHANGELOG.md) — version history.
8. [`cursor_setup.md`](cursor_setup.md) — IDE-specific notes.
9. [`AGENTS.md`](AGENTS.md) — technical notes for AI agents.

## Software methods and repository history

- [Canonical manuscript](manuscript/README.md) — local metadata organization, fixture evidence, and reproducibility.
- [Manuscript status](manuscript-status.md) — scope of the software methods note.
- [Diagrams](diagram.md) — repository and pipeline visuals.
- [Open maintenance items](TODO.md) — dated repository review with implementation evidence.
- [OpenAI refactor record](REAL_OPENAI_REFACTOR.md) — historical checklist. See the architecture guide for current behavior.

All documentation follows the conventions in [`.cursorrules`](../.cursorrules) and is kept in sync with code in `src/pipeline_orchestration.py` and `src/utils/config.py`.
