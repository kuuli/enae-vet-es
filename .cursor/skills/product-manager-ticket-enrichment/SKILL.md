---
name: product-manager-ticket-enrichment
description: Structures and sharpens Jira tickets through phased refinement—problem framing, scope, testable acceptance criteria, edge cases, dependencies, risks, and metrics. Use when enriching or grooming backlog items, rewriting vague acceptance criteria, running an /enrich workflow, or preparing issues for development handoff.
---

# Product manager: ticket enrichment

## When to use

Apply this skill when:

- Running the **enrich** workflow on a Jira issue.
- The user asks to improve, groom, refine, or “make shippable” a ticket.
- Acceptance criteria are missing, duplicated, untestable, or mixed with implementation detail.
- Scope, success metrics, or dependencies are unclear before engineering starts.

## Principles

1. **Outcome over output**: Tie work to user or business value, not only tasks.
2. **Testable AC**: Every criterion should be verifiable by QA or an automated check where possible.
3. **Explicit boundaries**: In scope / out of scope prevents gold-plating and scope creep.
4. **Single source of truth**: Enriched content should read as one coherent spec, not a pile of notes.
5. **Safe publishing**: Never overwrite Jira without explicit user approval; prefer comments or paste-back first.
6. **English**: All ticket artifacts produced by the agent are in **English** (match this repository’s engineering language).

## Phased enrichment model

Execute **in order**. Each phase builds on the previous. If the ticket is already strong in an area, keep that section brief and move on.

### Phase A — Diagnose

- Classify maturity: *idea*, *shaped*, *ready for refinement*, *ready for dev*.
- List **gaps**: missing problem statement, missing AC, ambiguous terms, missing error cases, missing NFRs, hidden dependencies.
- Flag **contradictions** between title, description, and AC.
- Note **assumptions** that should be validated with a stakeholder.

### Phase B — Structure

Produce or tighten:

- **Problem / opportunity**: Who is affected and why now?
- **Desired outcome**: What changes for the user or the business when this is done?
- **Scope**: In scope / out of scope (bullet lists).
- **User scenarios** (optional but recommended): Short “Given / When / Then” or user story + notes.
- **Constraints**: Technical, regulatory, brand, or timeline constraints that engineering must respect.

### Phase C — Acceptance criteria hardening

- Rewrite AC as a **numbered list** of atomic statements.
- Prefer **observable** language: “User can…”, “System returns…”, “When X then Y”.
- Add **negative paths** and **validation** (empty input, permissions, timeouts).
- Add **edge cases** only when they change behavior or are likely in production.
- Separate **implementation detail** from **behavior** unless the ticket is explicitly technical and the constraint is non-negotiable.

### Phase D — Delivery readiness

- **Dependencies**: Other tickets, teams, data, feature flags, environments.
- **Risks & mitigations**: Top 3 risks with one mitigation each.
- **Open questions**: Unresolved decisions; mark **must-answer before dev** vs **can defer**.
- **Metrics / signals** (if applicable): How we know we succeeded post-release.
- **Suggested breakdown**: Optional subtasks or slices for incremental delivery.

### Phase E — Quality gate (self-check)

Before presenting the final enriched ticket, verify:

- [ ] Title matches scope (or propose a better title).
- [ ] AC are **MECE** enough for development (no duplicate AC; minimal overlap).
- [ ] Every AC is **testable** or explicitly marked as *subjective / UX* with review owner.
- [ ] Out-of-scope items are stated where ambiguity was common.
- [ ] No clinical or legal claims are invented for a vet product; if domain facts are needed, cite `docs/` or ask the user.

## Output format

Deliver the enriched artifact using the template in **`reference.md`** unless the user specifies another format.

## Jira hygiene

- Prefer **one** clear description block and **one** AC section (avoid scattering the same requirement in three places).
- If the project uses custom fields for AC, mirror numbered AC there in comments or description per team convention—ask the user if unsure.
- Long enrichment: post a **summary** in a Jira comment and attach or link to the full markdown elsewhere if the team uses that pattern.

## Handoff to engineering

Close with:

- **Definition of Done** (short bullet list: code, tests, docs, feature flag, etc.—tailored to team norms).
- **Suggested first milestone** for the implement workflow (what to build first to reduce risk).

## Related project context

For **enae-vet-es**, align suggestions with `CLAUDE.md` and `docs/` (booking rules, pre-op messaging, bot safety). Do not invent veterinary protocols; point to existing docs or open questions.
