from app.graph.neo4j_client import neo4j_client


def create_company_department_relationships(departments: list):
    """Connects companies with their departments using HAS_DEPARTMENT relationships."""

    query = """
    UNWIND $departments AS department

    MATCH (c:Company {id: department.company_id})
    MATCH (d:Department {id: department.id})

    MERGE (c)-[:HAS_DEPARTMENT]->(d)
    """

    neo4j_client.execute_query(
        query, 
        {"departments": departments}
    )

def create_employee_company_relationships(employees: list):
    """Connects employees with their companies using WORKS_FOR relationships."""

    query = """
    UNWIND $employees AS employee

    MATCH (e:Employee {id: employee.id})
    MATCH (c:Company {id: employee.company_id})

    MERGE (e)-[:WORKS_FOR]->(c)
    """

    neo4j_client.execute_query(
        query, 
        {"employees": employees}
    )

def create_employee_department_relationships(employees: list):
    """Connects employees with their departments using BELONGS_TO relationships."""

    query = """
    UNWIND $employees AS employee

    MATCH (e:Employee {id: employee.id})
    MATCH (d:Department {id: employee.department_id})

    MERGE (e)-[:BELONGS_TO]->(d)
    """

    neo4j_client.execute_query(
        query, 
        {"employees": employees}
    )

def create_employee_skill_relationships(relationships: list):
    """Connects employees with their skills using HAS_SKILL relationships."""

    query = """
    UNWIND $relationships AS rel

    MATCH (e:Employee {id: rel.employee_id})
    MATCH (s:Skill {id: rel.skill_id})

    MERGE (e)-[:HAS_SKILL]->(s)
    """

    neo4j_client.execute_query(
        query, 
        {"relationships": relationships}
    )

def create_employee_project_relationships(relationships: list):
    """Connects employees with projects using WORKS_ON relationships."""

    query = """
    UNWIND $relationships AS rel

    MATCH (e:Employee {id: rel.employee_id})
    MATCH (p:Project {id: rel.project_id})

    MERGE (e)-[:WORKS_ON]->(p)
    """

    neo4j_client.execute_query(
        query, 
        {"relationships": relationships}
    )

def create_project_customer_relationships(relationships: list):
    """Connects projects with customers using SERVES relationships."""

    query = """
    UNWIND $relationships AS rel

    MATCH (p:Project {id: rel.project_id})
    MATCH (c:Customer {id: rel.customer_id})

    MERGE (p)-[:SERVES]->(c)
    """

    neo4j_client.execute_query(
        query, 
        {"relationships": relationships}
    )

def create_employee_manager_relationships(relationships: list):
    """Connects employees with managers using REPORTS_TO relationships."""

    query = """
    UNWIND $relationships AS rel

    MATCH (employee:Employee {id: rel.employee_id})
    MATCH (manager:Employee {id: rel.manager_id})

    MERGE (employee)-[:REPORTS_TO]->(manager)
    """

    neo4j_client.execute_query(
        query, 
        {"relationships": relationships}
    )

def create_task_project_relationships(tasks: list):
    """Connects tasks with their projects using BELONGS_TO relationships."""

    query = """
    UNWIND $tasks AS task

    MATCH (t:Task {id: task.id})
    MATCH (p:Project {id: task.project_id})

    MERGE (t)-[:BELONGS_TO]->(p)
    """

    neo4j_client.execute_query(
        query, 
        {"tasks": tasks}
    )

def create_task_employee_relationships(tasks: list):
    """Connects tasks with assigned employees using ASSIGNED_TO relationships."""

    query = """
    UNWIND $tasks AS task

    MATCH (t:Task {id: task.id})
    MATCH (e:Employee {id: task.assigned_to})

    MERGE (t)-[:ASSIGNED_TO]->(e)
    """

    neo4j_client.execute_query(
        query, 
        {"tasks": tasks}
    )

def create_project_company_relationships(projects: list):
    """Connects projects with their companies using BELONGS_TO relationships."""

    query = """
    UNWIND $projects AS project

    MATCH (p:Project {id: project.id})
    MATCH (c:Company {id: project.company_id})

    MERGE (p)-[:BELONGS_TO]->(c)
    """

    neo4j_client.execute_query(
        query, 
        {"projects": projects}
    )

def create_document_project_relationships(documents: list):
    """Connects documents with projects using DOCUMENTS relationships."""

    query = """
    UNWIND $documents AS document

    MATCH (d:Document {id: document.id})
    MATCH (p:Project {id: document.project_id})

    MERGE (d)-[:DOCUMENTS]->(p)
    """

    neo4j_client.execute_query(
        query, 
        {"documents": documents}
    )
