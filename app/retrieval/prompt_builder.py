def build_prompt(context_text: str, question: str) -> str:
    """Combines formatted graph context and the user's question into a single LLM prompt."""

    prompt = f"""You are an enterprise assistant. Use the context below to answer the question accurately.
    If the answer is not present in the context, say you don't have enough information.

    Context:
    {context_text}

    Question: {question}

    Answer:"""

    return prompt
