from app.retrieval.graph_retriever import GraphRetriever


class EntityResolver:
    """Resolves an entity type + name into a concrete graph ID."""

    def __init__(self):
        self.retriever = GraphRetriever()

        # Maps entity_type -> retriever method to call
        self.resolvers = {
            "employee": self.retriever.get_employee_by_name,
            "project": self.retriever.get_project_by_name,
            "customer": self.retriever.get_customer_by_name,
            "department": self.retriever.get_department_by_name,
            "company": self.retriever.get_company_by_name,
            "skill": self.retriever.get_skill_by_name,
            "document": self.retriever.get_document_by_title,
        }

    def resolve(self, entity_type: str, name: str) -> str | None:
        """Returns the ID of the best-matching entity, or None if not found or not resolvable by name."""

        resolver_fn = self.resolvers.get(entity_type)

        if resolver_fn is None:
            return None

        matches = resolver_fn(name)

        if not matches:
            return None

        return matches[0]["id"]

    def resolve_any(self, name: str):
        """Tries every known entity type and returns (entity_type, id) for the first match."""

        for entity_type, resolver_fn in self.resolvers.items():
            matches = resolver_fn(name)

            if matches:
                return entity_type, matches[0]["id"]

        return None, None

