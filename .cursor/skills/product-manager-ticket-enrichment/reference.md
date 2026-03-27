# Reference: enriched Jira ticket template

Use this structure for the **final consolidated output** of the enrich workflow. Omit sections that do not apply; keep headings for scanability.

```markdown
## Enriched ticket: <KEY> — <title>

### Metadata
- **Issue key**: …
- **Type**: …
- **Status**: …
- **Maturity** (before → after): …

### Summary (one paragraph)
…

### Problem / opportunity
…

### Desired outcome
…

### In scope
- …

### Out of scope
- …

### User scenarios
1. …

### Functional requirements
1. …

### Acceptance criteria
1. …
2. …

### Non-functional requirements (if any)
- …

### Edge cases & error handling
- …

### Dependencies
- …

### Risks & mitigations
| Risk | Mitigation |
|------|------------|
| … | … |

### Open questions
- [ ] **Must before dev**: …
- [ ] **Can defer**: …

### Metrics / success signals (if any)
- …

### Suggested breakdown (optional)
- …

### Definition of Done
- …

### Changelog vs original ticket
- **Added**: …
- **Clarified**: …
- **Removed / deferred**: …
```

## AC quality patterns

**Weak**: “The feature works.”  
**Strong**: “When a valid `session_id` and non-empty `msg` are POSTed to `/askbot`, the response is HTTP 200 and JSON includes `msg` and `session_id` matching the request.”

**Weak**: “Good UX.”  
**Strong**: “Validation errors return HTTP 4xx with a JSON or text `detail` field; the server does not return a 5xx for invalid input.” (Or: “UX review sign-off by @…” if subjective.)

## Numbering convention

- Use **1., 2., 3.** for AC engineering must satisfy.
- Use **R1, R2** only if the team reserves numbers for regulatory/traceability; otherwise avoid duplicate numbering schemes in one ticket.
