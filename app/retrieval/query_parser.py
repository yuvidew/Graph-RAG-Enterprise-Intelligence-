import json

from app.llm.client import LLMClient

ENTITY_TYPES = [
    "employee", "project", "task", "customer",
    "department", "company", "document", "skill",
]


class QueryParser:
    """Uses the LLM to extract the entity type and target name from a raw question."""

    def __init__(self):
        self.llm = LLMClient()

    def parse(self, question: str, previous_entity: dict | None = None) -> dict:
        """Returns {'entity_type': ..., 'name': ...} extracted from the question."""

        previous_context = ""
        if previous_entity:
            previous_context = f"""
Previous entity discussed: type={previous_entity['entity_type']}, name={previous_entity['name']}
If the question uses a vague reference like "this", "it", "that", or "the {previous_entity['entity_type']}"
instead of naming a new entity, reuse the previous entity's type and name above.
"""

        prompt = f"""Extract the entity type and the specific name mentioned in the question below.

Valid entity types: {", ".join(ENTITY_TYPES)}
{previous_context}
Respond with ONLY valid JSON, no extra text, no markdown, in this exact format:
{{"entity_type": "<one of the valid types>", "name": "<the name>"}}

Question: {question}
"""

        response = self.llm.generate(prompt)

        cleaned = response.strip().strip("`").strip()
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()

        return json.loads(cleaned)
