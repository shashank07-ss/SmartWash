# GitHub Copilot instructions for this repository

**Purpose:** Help AI coding agents be immediately productive in this repository by summarizing the project "big picture", discoverable workflows, file patterns, and safe change rules.

## Quick summary 🔍
- Minimal Flask-style web app: expected entrypoint `app.py`, Jinja2 templates under `templates/` (`login.html`, `register.html`, `dashboard.html`, `admin.html`) and static assets under `static/` (`style.css`, `images/`).
- Many files in the workspace are currently empty—**confirm behavior** with the repo owner before implementing assumptions.

## How to run locally (assumptions & commands) ⚙️
- Typical workflow (confirm with owner):
  - Create env: `python -m venv .venv && .venv/bin/pip install -r requirements.txt`
  - Run Flask: `export FLASK_APP=app.py && export FLASK_ENV=development && flask run`
  - Alternative: `python -m flask run` (if `FLASK_APP` is set)
- If you add dependencies, update `requirements.txt` and include a short note in the PR description.

## Key files & patterns to reference 🔧
- `app.py` — expected Python entrypoint for routes and app configuration.
- `templates/` — Jinja2 HTML templates for routes: `login`, `register`, `dashboard`, `admin`.
- `static/style.css` and `static/images/` — frontend assets.
- `requirements.txt` — Python deps (currently empty; update when adding libs).

## Project-specific conventions & rules ✅
- Assume Flask routing + Jinja2 templates unless the owner indicates otherwise.
- For each route you change/add, update the corresponding template in `templates/` and assets in `static/` as needed.
- Avoid committing secrets or environment variables; use `.env` or ask the owner how secrets should be managed.

## Tests, CI, linters, and missing artifacts ⚠️
- No test framework, CI config, or linters were found. Before adding tests or CI, ask the owner for preferred tooling (pytest, GitHub Actions workflows, black/flake8).
- If you add tests, include a short README section with run instructions and update PR description.

## When you make non-trivial changes 📝
- Add: implementation, minimal tests (if owner agrees), `requirements.txt` updates, and a README note explaining how to run changes.
- Keep PRs small and self-contained. In the PR description, list exact runtime commands you used to validate the change and any new env vars required.

## Discoverability tips for agents 🔎
- Check if files are empty before implementing behavior. If a file is empty (e.g., `app.py`), ask the owner: "Should I scaffold X or do you prefer I modify an existing app layout?"
- Search for routes by name (e.g., `login`, `register`, `dashboard`, `admin`) to find related templates and handlers.

## Merge behavior if this file already exists
- If `.github/copilot-instructions.md` exists, merge thoughtfully: preserve owner-written guidance and only add clarifying, repository-specific instructions. Keep the file short and actionable.

---

If anything here is unclear or you'd like more rules/examples from the codebase, tell me what to expand and I will iterate. Please confirm preferred runtime commands and testing tools so I can refine these instructions.