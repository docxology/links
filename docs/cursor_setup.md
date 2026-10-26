# Setting Up Cursor IDE

Cursor is an AI-powered code editor based on VS Code that helps streamline development workflows. This guide walks you through the installation and setup process.

## Installation

### macOS
1. Download from [cursor.com](https://cursor.com)
2. Open the installer and drag Cursor into Applications
3. Launch Cursor

### Windows
1. Download the `.exe` from [cursor.com](https://cursor.com)
2. Run the installer
3. Launch from the Start menu or desktop shortcut

### Linux
1. Download `.AppImage` or `.deb` from [cursor.com](https://cursor.com)
3. For AppImage:
   - Make it executable: `chmod +x Cursor-*.AppImage`
   - Run it: `./Cursor-*.AppImage`
4. For Debian/Ubuntu:
   - Install with: `sudo dpkg -i cursor_*.deb`
   - Launch from your applications menu

## Initial Setup

1. When you first open Cursor, you'll be prompted to log in or create an account
2. Sign in with GitHub or create a new Cursor account
3. Set up API keys:
   - Navigate to Settings → AI → API Keys
   - Add your OpenAI API key for enhanced AI capabilities

## Using Cursor with this Project

1. Open the project root in Cursor.
2. The `.cursorrules` and folder-level `AGENTS.md` / `README.md` files provide persistent guidance.
3. Use the AI chat (`/`) with references to specific files (e.g. `@src/pipeline_orchestration.py`).
4. Key commands:
   - `uv sync --all-extras`
   - `uv run pytest`
   - `uv run python -m src.main --only-extract`

Project-specific:
- Follow conventions in [`.cursorrules`](../.cursorrules) and [`AGENTS.md`](../AGENTS.md) in every folder.
- Documentation is in [`docs/`](../docs/) with hub at [`docs/README.md`](../docs/README.md).
- Tests prefer real data; live OpenAI tests are marked and excluded by default.

## Additional Resources

- [Cursor Documentation](https://docs.cursor.com)
- Root [`README.md`](../README.md) and [`docs/DEVELOPMENT.md`](DEVELOPMENT.md)

## Troubleshooting

- AI context: reference specific `@docs/ARCHITECTURE.md` or `@src/pipeline_orchestration.py`.
- Environment: ensure `.env` is loaded and `uv` is used.
- Linter errors after edits: run `uv run pytest` and check with ReadLints if needed.
 