# Enriched ticket: VETES-14 — [Doc VET-5] Enrich command / skill (tickets or specs)

**Source:** [VETES-14](https://kuuli.atlassian.net/browse/VETES-14)  
**Backlog reference:** VET-5  
**Enrichment date:** 2026-03-26 (Cursor agent, product-manager ticket enrichment skill)

---

### Metadata

- **Issue key**: VETES-14
- **Type**: Story
- **Status**: In Progress (at time of enrichment)
- **Maturity** (before → after): *Under-specified doc story* → *Ready for dev / doc review with testable acceptance criteria*

---

### Summary (one paragraph)

The team needs a **repeatable Cursor workflow** to refine Jira tickets (or specification text) **before** implementation: phased product thinking, clearer scope, and testable acceptance criteria. The deliverable lives **in this repository** as a **`/enrich`-style command**, a **product-manager-oriented skill**, and an **agent definition**, **decoupled** from the existing **implement** workflow while staying **structurally aligned** with it (same Jira MCP patterns, checklists, and handoff expectations). The story also requires a **concrete before/after example** so contributors see the value of enrichment.

---

### Problem / opportunity

- Tickets often ship with **vague goals**, **missing AC**, or **mixed scope**, which slows engineering and creates rework.
- Without a documented **enrich** path, grooming depends on individual habit rather than a shared, automatable workflow.
- Backlog item **VET-5** calls out this gap; **VET-4** (referenced in the original description) is the parallel “implement” track—**enrich** should mirror its rigor **without** bundling implementation steps into the same command.

---

### Desired outcome

Any team member can run an **enrich** invocation in Cursor, get a **phased** refinement of a Jira issue (diagnosis → structure → hardened AC → delivery readiness), and optionally **publish** back to Jira **only after explicit approval**. The repo contains **versioned** command + skill + agent docs, plus an **illustrative before/after** so onboarding is fast.

---

### In scope

- **Cursor command** documenting the full enrich workflow (prerequisites, phases, delegation to PM-style reasoning, publish options).
- **Product-manager skill** (`SKILL.md` + `reference.md` template) for phased enrichment and quality gate.
- **Product-manager agent** definition (`.cursor/agents/product-manager.md`) consistent with the existing backend agent pattern.
- **Independence from implement**: enrich does not trigger code generation, branch creation, or PR opening by default; it produces or updates **specifications**.
- **Alignment with implement / VET-4**: same Atlassian MCP usage style (e.g. `getAccessibleAtlassianResources`, `getJiraIssue`), phase/checklist discipline, and clear handoff (“run **implement** after AC stable”).
- **Before/after example** documented under `docs/jira/` (see companion file).
- **README** (and optionally `CLAUDE.md`) updated so **Cursor workflows** mention **Enrich** next to **Implement**.

### Out of scope

- Implementing application features unrelated to the enrich workflow.
- Automatic overwrite of Jira descriptions without user confirmation.
- Replacing Jira as the system of record (files in `docs/jira/` are **artifacts**, not a substitute for Jira for active sprint management).
- Defining clinical or veterinary domain rules (this story is **tooling / process** only).

---

### User scenarios

1. **PM / tech lead**: “Enrich VETES-14” → agent loads Jira issue, runs phased refinement, returns markdown; user chooses to paste, comment, or (if approved) update description.
2. **Developer**: Reads `docs/jira/VETES-14-before-after-example.md` to learn what “good” AC looks like before requesting enrich on their own tickets.
3. **Contributor**: Opens `.cursor/commands/enrich.md` to understand how PM delegation works (`generalPurpose` Task + agent file + skill).

---

### Functional requirements

1. Repository contains **`.cursor/commands/enrich.md`** describing the end-to-end enrich workflow.
2. Repository contains **`.cursor/skills/product-manager-ticket-enrichment/SKILL.md`** and **`reference.md`** with phased model and output template.
3. Repository contains **`.cursor/agents/product-manager.md`** with YAML frontmatter and role boundaries (no silent Jira overwrite).
4. **`docs/jira/VETES-14-before-after-example.md`** demonstrates a **before** (vague) and **after** (enriched) ticket fragment.
5. **README** includes a **Cursor workflows** bullet linking to **`enrich.md`** (alongside **implement**).

---

### Acceptance criteria

1. **Given** the repository on `main` (or the PR branch), **when** a reader opens `.cursor/commands/enrich.md`, **then** they find phased steps (ingest → diagnose → structure → AC → delivery readiness → consolidate → publish with approval) and explicit Atlassian MCP prerequisites consistent with `implement.md`.
2. **Given** the skill folder `product-manager-ticket-enrichment`, **when** they read `SKILL.md`, **then** they find phases **A–E**, principles (testable AC, explicit scope, English output, no silent Jira updates), and a quality gate checklist.
3. **Given** `reference.md`, **when** they use the template, **then** they can produce a consolidated enriched ticket artifact without ad-hoc formatting.
4. **Given** `product-manager.md`, **when** an agent follows it, **then** it must read the skill + reference and treat Jira updates as orchestrator + user-approved only.
5. **Given** `docs/jira/VETES-14-before-after-example.md`, **when** a new contributor reads it, **then** they see at least one **before** block (vague title + description) and one **after** block (structured problem, scope, numbered AC).
6. **Given** README **Cursor workflows**, **when** they scan the section, **then** both **Implement** and **Enrich / groom** are documented with links to the corresponding command files.
7. **Independence**: **Enrich** documentation does not require running **implement** or merging implement’s development phases into enrich; cross-reference is **handoff only** (“after enrich, run implement when ready”).

---

### Non-functional requirements

- **Discoverability**: File names and headings use clear, searchable terms (`enrich`, `product-manager`, `ticket-enrichment`).
- **Maintainability**: Command and skill cross-reference each other with **relative paths** under `.cursor/`.
- **Language**: All **new** engineering artifacts for this story are in **English** (Jira source may remain bilingual; enriched spec is English per repo convention).

---

### Edge cases & error handling

- **Missing Jira key**: Enrich command requires the user to supply a ticket key or URL; agent must ask rather than guess.
- **MCP unavailable**: Workflow documentation should state that Jira steps need Atlassian MCP; offline mode = user pastes ticket body manually (document as optional path in command if not already).
- **Huge tickets**: Consolidation may truncate for Jira comments; full body remains in `docs/jira/` or chat.

---

### Dependencies

- **Backlog**: VET-5 (parent reference in title).
- **Alignment**: VET-4 / implement workflow — structural parity (checklists, MCP, phases); exact VET-4 issue may live in another project or naming; treat **`.cursor/commands/implement.md`** as the canonical “implement” shape for this repo.
- **Cursor**: Task tool with `generalPurpose` (or future dedicated PM subagent if enabled).

---

### Risks & mitigations

| Risk | Mitigation |
|------|------------|
| Drift between **enrich** and **implement** commands | Cross-link “Relation to implement” sections; review both in the same PR when changing Jira patterns. |
| Users overwrite Jira by mistake | Enrich command mandates **explicit** publish option (A/B/C); default is chat-only or comment. |
| Example goes stale | Tie example to **VETES-14** and update in the same PR when the template changes. |

---

### Open questions

- [ ] **Must before dev**: Confirm **VET-4** issue key and project (VETES-4 not visible via API); update this doc with a concrete link when available.
- [ ] **Can defer**: Whether to add a **slash-command** alias in Cursor UI vs. natural-language only.

---

### Metrics / success signals

- Contributors report **fewer clarification rounds** on tickets that went through enrich.
- At least one **real** ticket enriched via the workflow and linked from a PR or Jira comment.

---

### Suggested breakdown (optional)

1. Add command + skill + agent files (may be one PR — this delivery).
2. Add `docs/jira` examples + README link.
3. Follow-up: optional Jira **comment** on VETES-14 pointing to the merged PR.

---

### Definition of Done

- [ ] `.cursor/commands/enrich.md` merged.
- [ ] `.cursor/skills/product-manager-ticket-enrichment/{SKILL.md,reference.md}` merged.
- [ ] `.cursor/agents/product-manager.md` merged.
- [ ] `docs/jira/VETES-14-enriched.md` (this file) and **`VETES-14-before-after-example.md`** merged.
- [ ] README updated with **Enrich** workflow bullet.
- [ ] PR opened with Jira key **VETES-14** in title/description.

---

### Changelog vs original ticket

- **Added**: Full phased spec, testable AC, risks, open questions, DoD, and traceability to VET-5 / VET-4 alignment intent.
- **Clarified**: “Independiente de implementar” → enrich is a **separate** command; **handoff** to implement is explicit, not bundled.
- **Removed / deferred**: Domain-specific vet booking requirements (not applicable to this tooling story).
