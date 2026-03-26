def build_prompt(question: str, retrieved_chunks: list) -> str:
    """
    Strict RAG prompt: model must answer ONLY from context.
    """

    context_blocks = []
    for i, chunk in enumerate(retrieved_chunks, 1):
        context_blocks.append(
            f"[Source {i}]\n{chunk['chunk_text']}"
        )

    context = "\n\n".join(context_blocks)

    prompt = f"""
You are a helpful AI assistant.

RULES:
- Answer ONLY using the information in the context.
- Do NOT use outside knowledge.
- If the answer is not present, say:
  "Answer not found in the provided document."

Context:
{context}

Question:
{question}

Answer:
""".strip()

    return prompt
