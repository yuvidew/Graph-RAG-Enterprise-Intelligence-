from neo4j import GraphDatabase

from app.core.config import settings


class Neo4jClient:
    """Provides a reusable Neo4j database connection and query execution interface."""
    
    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(
                settings.neo4j_username,
                settings.neo4j_password
            )
        )

    def execute_query(
        self,
        query: str,
        parameters: dict | None = None
    ):
        """Executes a Cypher query and returns all retrieved records."""

        with self.driver.session(
            database=settings.neo4j_database
        ) as session:

            result = session.run(
                query,
                parameters or {}
            )

            return [record.data() for record in result]

    def verify_connection(self):
        """Verifies that the Neo4j database is reachable and responding."""

        with self.driver.session(
            database=settings.neo4j_database
        ) as session:

            result = session.run("RETURN 1 AS test")

            return result.single()["test"]

    def close(self):
        self.driver.close()


neo4j_client = Neo4jClient()
