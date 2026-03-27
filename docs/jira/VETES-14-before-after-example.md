# Before / after example: ticket enrichment (VETES-14)

This file satisfies the **“ejemplo antes/después”** intent from [VETES-14](https://kuuli.atlassian.net/browse/VETES-14): a compact illustration of how the **enrich** workflow sharpens a ticket.

---

## Before (vague story)

**Title:** Better API for chat

**Description:**

> We should improve the bot API. Add endpoints. Make sure it works with sessions. Tests would be good.

**Why this is weak**

- No problem statement, user, or success signal.
- “Improve” and “works” are not observable.
- Scope is unbounded (which endpoints? which session semantics?).
- No acceptance criteria QA can execute.

---

## After (enriched fragment)

**Title:** FastAPI: session-scoped `POST /askbot` and static `GET /public/{path}` with path traversal protection

**Summary**

Expose a minimal HTTP surface for the clinic bot: serve safe static assets and accept chat turns keyed by `session_id`, with validation errors returning 4xx. Conversation context must persist per session in memory for the current process.

**In scope**

- `GET /public/{file_path:path}` from a `public/` directory with resolved-path checks preventing escape.
- `POST /askbot` accepting JSON or `application/x-www-form-urlencoded` with `msg` and `session_id` (no `python-multipart` dependency).
- Non-empty validation for `msg` and `session_id` before invoking the chain.

**Out of scope**

- Database persistence, authentication, production hardening, LangChain tools / `AgentExecutor`.

**Acceptance criteria**

1. Existing file under `public/` returns HTTP 200 and correct bytes for `GET /public/...`.
2. Any path resolving outside `public/` returns 404 and never reads arbitrary filesystem locations.
3. Valid `POST /askbot` returns 200 and JSON including bot `msg` and echoed `session_id`.
4. Missing or empty `msg` or `session_id` returns 4xx with a clear error payload; server does not crash.
5. Two sequential posts with the same `session_id` include prior turns in model context (verified via tests or observable reply behavior).

**Definition of Done**

- Automated tests cover happy path, validation, traversal, and session persistence.
- README or docs describe how to run the API locally.

---

## How this maps to the repo workflows

- Use **`.cursor/commands/enrich.md`** to turn a **before**-style ticket into an **after**-style spec (phased PM refinement).
- When AC are stable, use **`.cursor/commands/implement.md`** to drive code, branches, and PRs.

The example **after** block is illustrative; it mirrors patterns used in real clinic-bot tickets (e.g. tool-free chain constraints) but does not replace Jira as the source of truth for a specific issue.
