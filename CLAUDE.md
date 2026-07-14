# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Spendly — a Flask + SQLite expense tracker built as a step-by-step learning project. The codebase is an intentionally incomplete scaffold: some routes render real pages, others are placeholders explicitly marked as "coming in Step N" for the student to implement. `database/db.py` is currently just a comment describing the functions it should contain — it has not been written yet.

When asked to implement a feature here, check whether it corresponds to one of the placeholder routes/steps in `app.py` or `database/db.py` before designing a new approach — the shape of what's expected is often already sketched out in a comment or stub.

## Commands

```bash
source venv/bin/activate        # activate the existing virtualenv
pip install -r requirements.txt # flask, werkzeug, pytest, pytest-flask
python app.py                   # run dev server on http://localhost:5001 (debug=True)
pytest                          # run tests (no test files exist yet)
```

There is no build step, linter, or frontend toolchain — templates are server-rendered Jinja2, CSS/JS are static files included directly.

## Architecture

- **`app.py`** — single Flask app with all routes. Fully-implemented routes (`/`, `/register`, `/login`, `/terms`, `/privacy`) just render templates. Placeholder routes (`/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete`) return literal "coming in Step N" strings and are meant to be built out with real logic, likely backed by SQLite via `database/db.py`.
- **`database/db.py`** — not yet implemented. Per its own header comment, it's meant to expose:
  - `get_db()` — SQLite connection with `row_factory` and foreign keys enabled
  - `init_db()` — creates tables via `CREATE TABLE IF NOT EXISTS`
  - `seed_db()` — inserts sample dev data
  The resulting DB file is `expense_tracker.db` at the project root (gitignored, not yet created).
- **`templates/`** — Jinja2 templates extending `base.html`, which defines the nav/footer chrome and the `title`/`head`/`content`/`scripts` blocks. `register.html` and `login.html` already POST to `/register` and `/login` with `name`/`email`/`password` fields and render an `{% if error %}` block — auth logic in `app.py` should populate `error` and re-render on failure rather than introducing a different flash/redirect pattern.
- **`static/`** — `css/style.css` (single stylesheet, ~700 lines) and `js/main.js` (empty stub — no JS features built yet).

There is no authentication, session handling, or ORM in place yet — expect to add plain SQLite queries (via `sqlite3`) and Flask sessions/cookies for login state when implementing those steps.
