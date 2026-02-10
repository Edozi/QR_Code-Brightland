# Copilot instructions for Concert_QRCODE

This file captures the minimal, actionable knowledge an AI coding agent needs to be productive in this repository.

## Big picture
- Single backend service in `backend/` (FastAPI app) that verifies tickets via a Postgres database.
- `frontend/` is present but contains no code in this workspace snapshot.

## Key files
- `backend/main.py` — FastAPI app; exposes POST `/verify` which updates a ticket's `status` and `used_at` using a raw SQL `UPDATE ... RETURNING` statement.
- `backend/database.py` — SQLAlchemy engine and `SessionLocal` factory. Reads DB connection from `DATABASE_URL` environment variable.
- `backend/models.py` — SQLAlchemy declarative model `Ticket` (Postgres `UUID` column, `status`, `used_at`, `scanner_id`).

## Runtime & dev workflow (discoverable facts)
- The code expects a Postgres connection string in `DATABASE_URL`. Example (bash):

  export DATABASE_URL="postgresql://user:pass@host:5432/dbname"

- Start the API using Uvicorn (typical invocation, repo has no task runner):

  python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

- The FastAPI handlers are synchronous (`def`), and SQLAlchemy sessions are created via `SessionLocal()`.

## Patterns & conventions specific to this project
- Uses raw SQL via `sqlalchemy.text()` in `backend/main.py` for the critical verify operation. The update is written to be atomic and uses Postgres `NOW()` and `RETURNING`.
- Database schema is referenced directly (table `tickets`). The code assumes the `tickets` table exists with columns `id`, `status`, `used_at`, `scanner_id`.
- Model uses Postgres-specific `UUID` type (`sqlalchemy.dialects.postgresql.UUID`) — expect UUID values for `Ticket.id`.
- Sessions: the code opens and closes `SessionLocal()` manually and commits after `execute()`. In one code path it re-opens a session to check existence after the update attempt.

## Integration points & external deps (discoverable)
- Postgres database (via `DATABASE_URL`). SQL uses Postgres-specific features (`NOW()`, `RETURNING`).
- SQLAlchemy is used for engine, sessions, and models. FastAPI is the HTTP framework. A Postgres driver (e.g., `psycopg2-binary`) is required at runtime but is not declared in the repo.

## When editing or extending verify flow
- Keep the atomic `UPDATE ... RETURNING` approach when changing verification logic — it's the existing pattern to mark a ticket used in one statement.
- If you need to add checks, either extend the `WHERE` clause of the `UPDATE` or perform a separate `SELECT` before `UPDATE` (but prefer one-statement patterns for a single writer to avoid race conditions).

## Quick examples (copyable)
- Set DB and run server (bash):

  export DATABASE_URL="postgresql://user:pass@host:5432/db"
  python -m uvicorn backend.main:app --reload

- Verify endpoint sample payload (POST /verify): form or query parameters `ticket_id` and `scanner_id` (the handler expects them as parameters).

## Repository gaps and caveats (explicitly observable)
- There is no `requirements.txt`, no tests, and `README.md` is empty — environment setup and dependency list are not in-repo.
- Frontend is empty in this snapshot — no cross-component contracts are present in code.

## How Copilot should help here
- Prefer small, explicit edits to `backend/` files. Follow existing patterns: raw SQL `text()` usage for critical DB updates, manual `SessionLocal()` lifecycle, and Postgres idioms.
- When suggesting new dependencies, call out the exact package name (e.g., `psycopg2-binary`) and explain why it's needed.
- Don't assume migrations or an ORM-managed schema; changes to DB schema should include guidance for applying SQL to Postgres.

If anything here is unclear or you want me to include example `requirements.txt` or a startup script, tell me which format you prefer and I'll add it.
