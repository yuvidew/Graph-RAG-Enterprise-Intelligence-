from app.graph.neo4j_client import neo4j_client
from app.graph.schema import SCHEMA_QUERIES

def create_schema():
    with neo4j_client.driver.session() as session:
        for query in SCHEMA_QUERIES:
            session.run(query)

    print("Graph schema created successfully.")

def verify_connection():
    with neo4j_client.driver.session() as session:
        result = session.run("SHOW CONSTRAINTS")
        return list(result)

def close_connection():
    neo4j_client.close()
