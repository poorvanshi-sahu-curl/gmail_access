# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the app

`run.sh` is misnamed — it is a **Python orchestrator**, not a shell script. It installs deps, pulls `gemma3:4b`, starts Ollama, runs uvicorn, then runs Streamlit in the foreground:

```
python run.sh
```

To run components individually (from the repo root — imports are package-rooted, e.g. `from backend.routers import ...`):

```
uvicorn backend.main:app --reload --port 8000
streamlit run frontend/app.py
ollama serve              # must be running before backend handles LLM routes
```

First-time Gmail OAuth (opens a browser, writes `token.json`):

```
python auth_gmail.py
```

`fix_init.py` re-creates the empty `backend/**/__init__.py` files; only needed if package imports break.

There are no tests, linters, or build steps configured.

## Architecture

Three-process system: **Streamlit (8501) → FastAPI (8000) → Ollama (11434) + Gmail API**. The frontend is a thin HTTP client over `requests`; all logic lives in the backend.

**Routing layer** (`backend/routers/*.py`) — one router per capability (`emails`, `summarize`, `draft`, `search`, `categorize`), mounted under matching prefixes in `backend/main.py`. Each router is ~10 lines: validate via a Pydantic schema, delegate to a service, return the response model.

**Service layer** (`backend/services/`):
- `GmailService` wraps the Google API client. `__init__` runs the full OAuth dance (refresh `token.json`, otherwise `InstalledAppFlow.run_local_server`), so **constructing the service can block on a browser login**. `fetch_emails` returns parsed `Email` models, preferring `text/plain` parts and truncating body to 3000 chars.
- `GemmaService` calls `ollama.chat` against the model named by `settings.gemma_model`. Each public method (`summarize`, `draft_reply`, `search`, `categorize`) is just a prompt template — change behavior by editing the prompt strings.

**Important singleton pattern**: routers instantiate their service at module top level (`gmail = GmailService()`, `gemma = GemmaService()`). Consequences:
- Importing `backend.routers.emails` triggers Gmail OAuth immediately. The backend will not start cleanly until `token.json` is valid — run `auth_gmail.py` first on a fresh checkout.
- A stale/corrupt `token.json` is handled in `GmailService._authenticate` (caught and re-auth'd), but only if the file is non-empty.

**Config** (`backend/config.py`) — Pydantic `BaseSettings` reads `.env`. Knobs: `ollama_host`, `gemma_model` (default `gemma3:4b`), `max_emails` (default 20), `backend_url`. The frontend reads `BACKEND_URL` from the env directly, not via this settings object.

**Schemas** (`backend/models/schemas.py`) — request/response models are paired per endpoint (`SummarizeRequest`/`SummarizeResponse`, etc.). The `Email` model is the canonical email shape returned by `/emails/` and consumed by the frontend.

## Secrets and local files

`credentials.json` (OAuth client) and `token.json` (user token) live at the repo root and are required for Gmail access. Treat them as secrets — do not commit changes that expose their contents.

<!-- code-review-graph MCP tools -->
## MCP Tools: code-review-graph

**IMPORTANT: This project has a knowledge graph. ALWAYS use the
code-review-graph MCP tools BEFORE using Grep/Glob/Read to explore
the codebase.** The graph is faster, cheaper (fewer tokens), and gives
you structural context (callers, dependents, test coverage) that file
scanning cannot.

### When to use graph tools FIRST

- **Exploring code**: `semantic_search_nodes` or `query_graph` instead of Grep
- **Understanding impact**: `get_impact_radius` instead of manually tracing imports
- **Code review**: `detect_changes` + `get_review_context` instead of reading entire files
- **Finding relationships**: `query_graph` with callers_of/callees_of/imports_of/tests_for
- **Architecture questions**: `get_architecture_overview` + `list_communities`

Fall back to Grep/Glob/Read **only** when the graph doesn't cover what you need.

### Key Tools

| Tool | Use when |
| ------ | ---------- |
| `detect_changes` | Reviewing code changes — gives risk-scored analysis |
| `get_review_context` | Need source snippets for review — token-efficient |
| `get_impact_radius` | Understanding blast radius of a change |
| `get_affected_flows` | Finding which execution paths are impacted |
| `query_graph` | Tracing callers, callees, imports, tests, dependencies |
| `semantic_search_nodes` | Finding functions/classes by name or keyword |
| `get_architecture_overview` | Understanding high-level codebase structure |
| `refactor_tool` | Planning renames, finding dead code |

### Workflow

1. The graph auto-updates on file changes (via hooks).
2. Use `detect_changes` for code review.
3. Use `get_affected_flows` to understand impact.
4. Use `query_graph` pattern="tests_for" to check coverage.
