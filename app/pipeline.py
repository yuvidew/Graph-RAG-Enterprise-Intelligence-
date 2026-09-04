from app.retrieval.entity_resolver import EntityResolver
from app.retrieval.context_builder import GraphContextBuilder
from app.retrieval.context_formatter import (
    format_employee_context,
    format_project_context,
    format_task_context,
    format_customer_context,
    format_department_context,
    format_company_context,
    format_document_context,
    format_skill_context,
)
from app.retrieval.prompt_builder import build_prompt
from app.llm.client import LLMClient

from app.retrieval.query_parser import QueryParser


class RAGPipeline:
    """Orchestrates the full GraphRAG flow: resolve entity -> build context -> format -> prompt -> generate answer."""

    def __init__(self):
        self.resolver = EntityResolver()
        self.builder = GraphContextBuilder()
        self.llm = LLMClient()
        self.parser = QueryParser()
        self.last_entity = None  # {"entity_type": ..., "name": ...}



        # Map entity tpe -> (builder_menthod, formatter_function)
        self.pipelines = {
            "employee": (self.builder.build_employee_context, format_employee_context),
            "project": (self.builder.build_project_context, format_project_context),
            "task": (self.builder.build_task_context, format_task_context),
            "customer": (self.builder.build_customer_context, format_customer_context),
            "department": (self.builder.build_department_context, format_department_context),
            "company": (self.builder.build_company_context, format_company_context),
            "document": (self.builder.build_document_context, format_document_context),
            "skill": (self.builder.build_skill_content, format_skill_context),
        }

    def _run(self, entity_type: str, name: str, question: str) -> dict:
        """Internal: resolves entity, builds context, gets the answer. Returns full detail dict."""

        if entity_type not in self.pipelines:
            raise ValueError(f"Unknown entity type: {entity_type}")

        entity_id = self.resolver.resolve(entity_type, name)

        if entity_id is None:
            # The guessed entity type might be wrong — search all types
            fallback_type, fallback_id = self.resolver.resolve_any(name)

            if fallback_id is not None:
                entity_type = fallback_type
                entity_id = fallback_id

        if entity_id is None:
            return {
                "entity_type": entity_type,
                "name": name,
                "entity_id": None,
                "context_text": None,
                "answer": f"Could not find anything matching '{name}'.",
            }

        self.last_entity = {"entity_type": entity_type, "name": name}

        build_fn, format_fn = self.pipelines[entity_type]

        context = build_fn(entity_id)
        context_text = format_fn(context)

        prompt = build_prompt(context_text, question)
        answer = self.llm.generate(prompt)

        return {
            "entity_type": entity_type,
            "name": name,
            "entity_id": entity_id,
            "context_text": context_text,
            "answer": answer,
        }

    def answer(self, entity_type: str, name: str, question: str) -> str:
        """Runs the full pipeline and returns the LLM-generated answer."""

        return self._run(entity_type, name, question)["answer"]

    def ask(self, question: str) -> str:
        """Takes a raw question, auto-detects entity type & name, then answers it."""

        parsed = self.parser.parse(question, previous_entity=self.last_entity)

        return self._run(parsed["entity_type"], parsed["name"], question)["answer"]

    def ask_debug(self, question: str) -> dict:
        """Like ask(), but returns full pipeline details (entity resolved, context, answer) — for eval/debugging."""

        parsed = self.parser.parse(question, previous_entity=self.last_entity)

        result = self._run(parsed["entity_type"], parsed["name"], question)
        result["question"] = question
        result["parsed_entity_type"] = parsed["entity_type"]

        return result
