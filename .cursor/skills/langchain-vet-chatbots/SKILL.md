---
name: langchain-vet-chatbots
description: Guides building LangChain chatbots with system prompts, tools, RAG, and memory for veterinary clinics. Use when creating or refining vet-clinic assistants, RAG over clinic protocols or drug data, tool-calling bots for appointments or patient lookup, or conversation memory in a veterinary context.
---

# LangChain Chatbots for Veterinary Clinics

## When to Use This Skill

Apply when:
- Building or refactoring a chatbot for a veterinary clinic (reception, triage, staff assistant).
- Designing system prompts, tools, RAG pipelines, or memory for such a bot.
- Working with LangChain (or LangGraph) in this project or any vet-sector codebase.

---

## 1. System Prompts

**Role and scope**
- Define a single role: e.g. "Reception assistant", "Clinical support bot", "Triage helper". Do not mix medical diagnosis with front-desk tasks in one prompt.
- State clearly that the bot does not replace a veterinarian and cannot diagnose; it supports scheduling, FAQs, and internal procedures.

**Veterinary-specific instructions**
- Use consistent terminology: patient (animal), client (owner), appointment, record, protocol, treatment, prescription.
- Include boundaries: no dosage or treatment advice beyond what is in the provided RAG/tools; escalate to staff for emergencies or unclear cases.
- Optional: list species or services the clinic supports so the bot stays on-scope.

**Safety and compliance**
- Add a short line that the bot must not invent drugs, dosages, or procedures; it should cite tools or retrieved documents when giving procedural or clinical information.

**Example prompt skeleton**

```markdown
You are [role] for [Clinic Name]. You help with [scope: e.g. appointments, common questions, internal protocols].
- Use "patient" for the animal, "client" for the owner.
- You do not diagnose or prescribe. For medical advice or emergencies, direct the user to contact the clinic or a vet.
- When explaining procedures or protocols, base your answer only on the information provided by your tools or retrieved documents; do not invent steps or dosages.
```

---

## 2. Tools

**Typical tools for a vet-clinic bot**
- **Appointments**: get today’s schedule, find next available slot, create/cancel appointment (if the backend exists).
- **Patients/Records**: search patient by name or ID, get last visit or next due treatment (e.g. vaccinations).
- **Knowledge**: internal protocols (e.g. pre-op checklist, discharge instructions), drug/formulary lookup (from RAG or a dedicated tool).

**Design**
- One tool per capability; keep function names and descriptions clear so the LLM can choose correctly (e.g. `get_todays_appointments`, `search_patient_by_name`).
- Return structured data (e.g. list of appointments with time, client, patient); the system prompt can tell the bot to summarize in natural language.
- For sensitive data (patient details), document access control and avoid logging PII in tool payloads.

**LangChain**
- Implement tools as LangChain tools (e.g. `@tool` or `StructuredTool`); bind them to the chat model with `bind_tools` and use an appropriate agent or invocation loop that handles tool calls and results.

---

## 3. RAG (Retrieval-Augmented Generation)

**What to index (vet context)**
- Internal protocols and SOPs (e.g. surgery prep, hospitalization, discharge).
- Drug/formulary information or approved reference texts (if licensed for internal use).
- FAQ or client-facing material (e.g. opening hours, payment, common questions).
- Do not put raw client/patient identifiable data into the RAG index unless required and compliant.

**Chunking**
- Use semantic chunking (e.g. by section or paragraph) so that retrieval returns full procedures or coherent passages.
- For tables (e.g. drug dosages), keep rows or small tables in one chunk to avoid splitting critical data.

**Retrieval**
- Use a vector store (e.g. from LangChain integrations) with embeddings; add metadata filters when relevant (e.g. document type, species).
- Retrieve a small number of highly relevant chunks (e.g. top 3–5); instruct the system prompt to base answers only on retrieved context and to say "I don’t have that information" when context is missing.

**Pipeline**
- In LangChain: load documents → split → embed → store; at query time: embed query → retrieve → pass context into the prompt (e.g. as a "context" or "sources" section).

---

## 4. Memory

**Conversation memory**
- Use LangChain’s conversation buffer or window memory so the bot has recent turns (and, if needed, a summary of older context) to keep dialogue coherent (e.g. "the dog we talked about", "that appointment").

**Scoping (optional)**
- For patient-specific flows, consider a separate store or namespace keyed by session/patient so that context is not mixed between clients.
- Do not persist full conversation logs with PII without a clear retention and access policy.

**Implementation**
- Add the chosen memory to the chain or agent (e.g. `ConversationBufferWindowMemory`, or a custom store). Ensure the prompt template includes the memory variable (e.g. `chat_history`).

---

## 5. Putting It Together

**Suggested order**
1. Define the system prompt (role, scope, vet terminology, safety).
2. Add tools (appointments, patient lookup, protocol/knowledge) and connect them to the model.
3. Add RAG if the bot must answer from clinic documents; connect retrieval output to the prompt.
4. Add conversation memory and wire it into the prompt.

**Testing**
- Test with realistic vet scenarios: booking an appointment, asking about a protocol, asking for drug info (only from RAG/tools), and edge cases (emergency, unknown patient, out-of-scope question).
- Verify the bot refuses to invent medical or dosage information and cites sources when giving procedural answers.

---

## Additional resources

- For LangChain API patterns and vet terminology reference, see [reference.md](reference.md).


---

## Summary Checklist

- [ ] System prompt defines one role, vet terminology, and "no diagnosis / no inventing" rule.
- [ ] Tools are single-purpose and return structured data; PII handling is considered.
- [ ] RAG sources are appropriate (protocols, FAQs, reference); chunks are coherent; retrieval count is limited.
- [ ] Conversation memory is attached and used in the prompt.
- [ ] Behaviour tested for common flows and for refusing to invent clinical content.
