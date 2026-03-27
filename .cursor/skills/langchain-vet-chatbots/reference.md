# LangChain Vet Chatbot — Reference

Use this file when you need concrete LangChain patterns or API details beyond [SKILL.md](SKILL.md).

## System prompt injection

- Pass the system message as the first message with `role="system"` in the messages list, or use the model’s native system parameter if available (e.g. `ChatOpenAI(..., system=...)` or `messages=[SystemMessage(content=...), ...]`).

## Tools

- Define tools with `@tool` or `StructuredTool`; describe parameters and return behaviour in the docstring so the model can choose and call them correctly.
- Use `model.bind_tools(tools)` and invoke with tool_choice as needed; handle `tool_calls` in the response and append tool results as message chunks, then call the model again until no more tool calls.

## RAG

- Loaders: `DirectoryLoader`, `PyPDFLoader`, etc. → split with `RecursiveCharacterTextSplitter` (or similar) → embed with `OpenAIEmbeddings` / other → store in `Chroma`, `FAISS`, or another vector store.
- Retrieval: `vectorstore.as_retriever().invoke(query)` (or `get_relevant_documents`); pass the retrieved text into the prompt as context.
- Prefer a chain that: embed query → retrieve → format context → call LLM with context + query.

## Memory

- `ConversationBufferWindowMemory(k=N)` for last N turns; or `ConversationSummaryMemory` for longer sessions.
- Add to the chain and ensure the prompt template has a placeholder for `chat_history` (or the variable name your memory uses).

## Veterinary terms (consistent in prompts)

| Use this | Not |
|----------|-----|
| patient (animal) | pet, animal (in formal context) |
| client (owner) | owner, customer |
| appointment / visit | booking, session |
| record / clinical record | file, history |
| protocol / SOP | procedure, steps |
| treatment / prescription | meds, drugs (when referring to prescribed treatment) |
