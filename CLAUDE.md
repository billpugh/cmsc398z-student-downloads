# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the course materials repository for **CMSC 398z** ("Effective Use of AI Coding Tools") at the University of Maryland, taught Fall 2025 by Bill Pugh (Emeritus CS Professor) and Derek Willis (Journalism). Materials are organized by week (`week1/` through `week14/`).

The file `AICSEPAR2026.md` is a Marp slide deck for a conference presentation about the course. It uses `---` as slide separators and Marp-specific directives.

## Project Structure

Each week directory contains a `README.md` with instructions, slides, and links. Some weeks contain standalone Python projects with their own `pyproject.toml` and `.venv/`. Projects are independent — there is no shared build system or top-level package manager.

## Running Projects

Individual projects use `uv` for dependency management:
```bash
cd week4/foreclosures
uv sync          # install dependencies
uv run python augment_foreclosures.py
uv run pytest    # run tests (where tests exist)
```

Some projects (weeks 5, 7) use Simon Willison's `llm` CLI tool for LLM API calls.

## Key Weekly Projects

- **Weeks 1-3**: Python learning projects (Wordle, Markov text, poker analysis) — these have `.github/copilot-instructions.md` files configuring AI to act as a tutor/coach rather than a solution provider
- **Week 4**: Foreclosure data parsing with noisy CSV/JSON data, geocoding, pydantic
- **Weeks 5-6**: Structured data extraction using LLMs via `llm` tool
- **Week 7**: Database/SQL projects with vector embeddings and semantic search
- **Weeks 8-10**: Working with large codebases (CPython IDLE editor, Congressional Record parser)
- **Weeks 11-12**: Full-stack social media app (Flask + SQLite, then JS frontend + REST API)
- **Weeks 13-14**: Working on quuly (React/Go/GraphQL office hours system)

## Copilot Instructions (Weeks 1-3)

Early-week projects include `.github/copilot-instructions.md` that enforce a coaching/tutoring mode. Key rules:
- Act as a coach, not a solution provider
- Don't write complete functions unless the student has described the logic in English first
- Use `TODO(student)` comments to guide structure
- Ask students what functions should return before implementing
- Use the `★ Insight` format for educational callouts

## Conventions

- Python projects use `uv` and `pyproject.toml` (not pip/requirements.txt)
- `.venv/` directories are gitignored
- Students submit work to UMD's submit server via `java -jar submit.jar`
- Chat transcripts saved as `chat.md` in project directories
