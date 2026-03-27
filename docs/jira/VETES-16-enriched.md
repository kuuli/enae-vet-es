# Enriched ticket: VETES-16 — Chatbot v4 API (FastAPI placeholders only)

**Source:** [VETES-16](https://kuuli.atlassian.net/browse/VETES-16)  
**Backlog reference:** VET-7  
**Enrichment:** Cursor enrich workflow — Chatbot v4 OpenAPI contract, placeholders only (no real UI, no LangChain).

---

### Metadata

- **Issue key**: VETES-16
- **Type**: Story
- **Status**: IN REVIEW (at time of enrichment)
- **Maturity** (before → after): *Generic “2 mock routes + Pydantic + /docs”* → *Contract-driven Chatbot v4 surface (`GET /`, `POST /ask_bot`) with explicit stub behaviour and testable AC*

---

### Summary (one paragraph)

Deliver a **minimal FastAPI** application that matches the **Chatbot v4** OpenAPI contract: a **placeholder HTML** response on `GET /` (reserved for a future visual chat UI) and a **placeholder JSON** response on `POST /ask_bot` accepting **`application/x-www-form-urlencoded`** fields `msg` and `session_id` (reserved for future LangChain integration). **No** rich front-end, **no** bot logic, **no** persistent session semantics beyond echoing inputs in the stub — only HTTP stubs, Pydantic/OpenAPI accuracy, and documentation so the next tickets can swap implementations without changing routes or content types.

---

### Enrichment trace (phases A–E)

#### Phase A — Diagnose

- **Maturity:** Previously “shaped” for a generic placeholder API; **insufficient** for the Chatbot v4 contract (paths and request encoding differ).
- **Gaps:** Missing `GET /` (`text/html`); missing `POST /ask_bot` (`x-www-form-urlencoded`); OpenAPI `info` should reflect **Chatbot v4** / `0.1.0`; `200` JSON schema for `ask_bot` was `{}` — **not testable**; no stated validation for empty `msg`; no decision on **`python-multipart`** vs manual urlencoded parsing.
- **Contradictions:** Existing repo work on VETES-16 may expose `/health` and `POST /api/v1/echo` (JSON body) — **not** in the Chatbot v4 YAML. Implementation must **align** with this enriched spec (replace or relocate routes).
- **Assumptions to validate:** Product accepts **snake_case** path `ask_bot` as the public contract; **English** for code and API docs; **stub** JSON shape below is acceptable until LangChain lands.

#### Phase B — Structure

- **Problem / opportunity:** We need a **stable HTTP contract** for the web channel before investing in UI and LangChain; early drift between OpenAPI and code is costly.
- **Desired outcome:** Developers and QA can hit **`/`** and **`/ask_bot`**, see correct **content types**, and rely on **Swagger `/docs`** that matches the contract; future work plugs into the same paths.
- **In scope:** Two routes only; FastAPI auto OpenAPI; README/run instructions; automated smoke tests; **no** `python-multipart` dependency (**recommended**): parse urlencoded body with **`urllib.parse.parse_qs`** from raw bytes (same pattern as VETES-1-style constraints).
- **Out of scope:** Real chat UI (widgets, streaming, CSS/JS apps); LangChain, tools, RAG, LLM calls; durable session store; auth, quotas, production deployment hardening.

#### Phase C — Acceptance criteria hardening

See **Acceptance criteria** below (numbered, observable).

#### Phase D — Delivery readiness

- **Dependencies:** VET-7 backlog intent; Chatbot v4 YAML (appendix); optional follow-up tickets for UI and LangChain.
- **Risks:** OpenAPI document in Jira vs repo drift; default `session_id=default` hiding missing client IDs — mitigated by validation rules in AC.
- **Open questions:** Whether to keep legacy `/health` for ops (defer unless SRE requires it).

#### Phase E — Quality gate

- [x] Title can remain under VETES-16 with description updated to reference **Chatbot v4** (or rename summary to include “Chatbot v4” — optional).
- [x] AC are atomic and testable.
- [x] Out of scope explicitly excludes UI and LangChain.
- [x] No veterinary clinical content invented (tooling-only ticket).

---

### Problem / opportunity

The team needs a **published API shape** for the clinic chatbot channel **before** building the interactive UI and LangChain pipeline. Without a frozen contract, front-end and back-end work will diverge.

---

### Desired outcome

- **`GET /`** returns **minimal placeholder HTML** (`200`, `Content-Type: text/html`) so a future UI can be served from the same route.
- **`POST /ask_bot`** accepts **form-urlencoded** `msg` and `session_id`, returns **JSON** with a **defined stub payload** (`200`).
- **OpenAPI/Swagger** at `/docs` documents both operations consistently with runtime behaviour.
- **README** explains how to run with **uvicorn** and how to try both endpoints.

---

### In scope

- FastAPI app with **`info.title` = `Chatbot v4`**, **`info.version` = `0.1.0`** (or equivalent in `FastAPI(...)` metadata).
- **`GET /`**: static **placeholder** HTML string (e.g. a short page stating “placeholder for future chat UI”).
- **`POST /ask_bot`**: read **`application/x-www-form-urlencoded`**; validate **`msg`** and **`session_id`** are present and **non-empty strings** after strip; respond with JSON stub (see AC).
- **Pydantic** models for the JSON response (and optional internal parsing types).
- **Tests**: `httpx`/`TestClient` covering happy path, `Content-Type`, and validation errors (`422` or `400` — pick one and document).
- **Dependencies:** **`requirements.txt`** remains the install path; **do not add `python-multipart`** — use **manual** urlencoded parsing from `Request.body()`.

### Out of scope

- Any **real** chat UI (beyond minimal HTML placeholder on `/`).
- **LangChain**, agents, tools, memory, or external APIs.
- Database or cross-request session persistence.
- Changing the **path names** or **HTTP methods** from the Chatbot v4 YAML.

---

### User scenarios

1. **Developer** runs `uvicorn`, opens `/docs`, sees **Home** (`GET /`) and **Ask Bot** (`POST /ask_bot`) with correct media types.
2. **QA** posts `msg` and `session_id` as **form fields** and receives **JSON** with echoed values and `placeholder: true`.
3. **Future UI ticket** replaces the HTML body of `GET /` without renaming the route.

---

### Functional requirements

1. Expose **`GET /`** with operation summary **Home**; response **`text/html`**; HTTP **200**.
2. Expose **`POST /ask_bot`** with summary **Ask Bot**; request **`application/x-www-form-urlencoded`**; fields **`msg`**, **`session_id`**; response **`application/json`** HTTP **200** on valid input.
3. Runtime **OpenAPI** (Swagger UI `/docs`) lists both paths and matches the contract above.
4. **Validation:** If `msg` or `session_id` is missing, empty, or not a string, return **4xx** with a **clear** error detail; do not invoke future bot logic (none exists in this ticket).

---

### Acceptance criteria

1. **GET /** returns **200**, **`Content-Type`** includes **`text/html`**, body is **non-empty** HTML and includes plain text indicating a **placeholder** for a future chat UI.
2. **POST /ask_bot** with header **`Content-Type: application/x-www-form-urlencoded`** and body `msg=hello&session_id=s1` returns **200** and JSON body **`{"msg": "hello", "session_id": "s1", "placeholder": true}`** (exact key order not required).
3. **POST /ask_bot** with missing **`msg`** or **`session_id`**, or with either field **whitespace-only**, returns **422** (or **400** if consistently documented) and **does not** return **200**.
4. **POST /ask_bot** with **`Content-Type: application/json`** returns **415** or **422** with a clear message (only urlencoded is supported in this contract).
5. **`GET /openapi.json`** includes paths **`/`** and **`/ask_bot`** with expected methods and content types.
6. **README** documents **`uvicorn main:app`** (or the chosen module path), **`/docs`**, and **curl** examples for **GET /** and **POST /ask_bot** (form body).
7. **No `python-multipart`** dependency is added to **`requirements.txt`**; urlencoded parsing uses **stdlib** (`urllib.parse`) or equivalent without multipart middleware.

---

### Non-functional requirements (if any)

- Code, comments, and OpenAPI descriptions in **English**.
- Handlers stay **thin** (no business rules beyond validation and stub response).

---

### Edge cases & error handling

- **Wrong content type** on `POST /ask_bot` → reject with **415/422** and explicit detail.
- **Very long `msg`** → optional max length (e.g. 2000 chars) returning **422**; if not enforced in this ticket, document as **follow-up** (open question).
- **Duplicate form keys** → last value wins (document behaviour).

---

### Dependencies

- **VET-7** (backlog reference in original Jira description).
- **Chatbot v4 OpenAPI YAML** (see appendix) — source of truth for paths and encodings.
- **Repository:** alignment with [main.py](https://github.com/kuuli/enae-vet-es/blob/main/main.py) after implement pass (may currently expose different routes).

---

### Risks & mitigations

| Risk | Mitigation |
|------|------------|
| Drift between appendix YAML and FastAPI-generated schema | Single source: implement from this doc; optionally add CI check comparing `openapi.json` to a pinned snapshot later. |
| Teams assume `placeholder: true` means “bot ready” | Document in README that **LangChain is out of scope** for this ticket. |
| Default `session_id` in old OpenAPI examples hides bugs | AC requires **non-empty** fields; reject whitespace-only. |

---

### Open questions

- [ ] **Must before dev:** Confirm whether **legacy `/health`** (or similar) must remain for probes alongside Chatbot v4 routes.
- [ ] **Can defer:** Maximum **`msg`** length and rate limiting.

---

### Metrics / success signals (if any)

- `/docs` loads and shows **two** operations; pytest green on stub + validation cases.

---

### Suggested breakdown (optional)

1. **Implement** routes + tests + README (implement workflow / PR).
2. **Future:** Ticket for **HTML chat UI** on `GET /`.
3. **Future:** Ticket for **LangChain** behind `POST /ask_bot`.

---

### Definition of Done

- [ ] `GET /` and `POST /ask_bot` implemented per AC (in code — **separate implement PR** after this enrichment).
- [ ] Tests and README updated.
- [ ] No LangChain/UI beyond placeholders.
- [ ] This enriched document merged under **`docs/jira/VETES-16-enriched.md`**.

---

### Changelog vs original ticket

- **Added:** Chatbot v4 OpenAPI contract (appendix); explicit **urlencoded** `ask_bot`; **HTML** home; **stub JSON** shape; **no multipart** implementation strategy; reconciliation note vs `/health` + `/api/v1/echo`.
- **Clarified:** “Two mock routes” → **specific paths and media types** per OpenAPI.
- **Removed / deferred:** Real UI and LangChain logic (explicitly out of scope).

---

## Appendix — Chatbot v4 OpenAPI (source YAML)

```yaml
openapi: 3.1.0
info:
  title: Chatbot v4
  version: 0.1.0
paths:
  /:
    get:
      summary: Home
      operationId: home_get
      responses:
        '200':
          description: Successful Response
          content:
            text/html:
              schema:
                type: string
  /ask_bot:
    post:
      summary: Ask Bot
      operationId: ask_bot_ask_bot_post
      requestBody:
        content:
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/Body_ask_bot_ask_bot_post'
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
components:
  schemas:
    Body_ask_bot_ask_bot_post:
      properties:
        msg:
          type: string
          default: ''
          title: Msg
        session_id:
          type: string
          default: default
          title: Session Id
      type: object
```

**Note:** The enriched AC above **replaces** `schema: {}` for the `200` JSON response with a **concrete stub schema** for QA. The appendix YAML is preserved as the **starting contract** from product/engineering.
