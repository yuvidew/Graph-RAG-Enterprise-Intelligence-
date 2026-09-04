from app.graph.neo4j_client import neo4j_client

def create_companies(companies: list):
    """Creates or updates Company nodes in Neo4j from JSON data."""

    query = """
    UNWIND $companies AS company
    MERGE (c:Company {id: company.id})
    SET
        c.name = company.name,
        c.industry = company.industry,
        c.location = company.location,
        c.description = company.description
    """

    neo4j_client.execute_query(
        query,
        {"companies": companies}
    )

def create_customers(customers: list):
    """Creates or updates Customer nodes in Neo4j from JSON data."""

    query = """
    UNWIND $customers AS customer
    MERGE (c:Customer {id: customer.id})
    SET
        c.name = customer.name,
        c.email = customer.email,
        c.industry = customer.industry,
        c.location = customer.location
    """

    neo4j_client.execute_query(
        query,
        {"customers": customers}
    )

def create_departments(departments: list):
    """Creates or updates Department nodes in Neo4j from JSON data."""

    query = """
    UNWIND $departments AS department
    MERGE (d:Department {id: department.id})
    SET
        d.name = department.name,
        d.description = department.description,
        d.company_id = department.company_id
    """

    neo4j_client.execute_query(
        query,
        {"departments": departments}
    )

def create_employees(employees: list):
    """Creates or updates Employee nodes in Neo4j from JSON data."""

    query = """
    UNWIND $employees AS employee
    MERGE (e:Employee {id: employee.id})
    SET
        e.name = employee.name,
        e.role = employee.role,
        e.email = employee.email,
        e.company_id = employee.company_id,
        e.department_id = employee.department_id
    """

    neo4j_client.execute_query(
        query,
        {"employees": employees}
    )

def create_skills(skills: list):
    """Creates or updates Skill nodes in Neo4j from JSON data."""

    query = """
    UNWIND $skills AS skill
    MERGE (s:Skill {id: skill.id})
    SET
        s.name = skill.name,
        s.category = skill.category,
        s.description = skill.description
    """

    neo4j_client.execute_query(
        query,
        {"skills": skills}
    )

def create_projects(projects: list):
    """Creates or updates Project nodes in Neo4j from JSON data."""

    query = """
    UNWIND $projects AS project
    MERGE (p:Project {id: project.id})
    SET
        p.name = project.name,
        p.description = project.description,
        p.category = project.category,
        p.status = project.status,
        p.company_id = project.company_id
    """

    neo4j_client.execute_query(
        query,
        {"projects": projects}
    )

def create_tasks(tasks: list):
    """Creates or updates Task nodes in Neo4j from JSON data."""

    query = """
    UNWIND $tasks AS task
    MERGE (t:Task {id: task.id})
    SET
        t.title = task.title,
        t.description = task.description,
        t.status = task.status,
        t.priority = task.priority,
        t.project_id = task.project_id,
        t.assigned_to = task.assigned_to
    """

    neo4j_client.execute_query(
        query,
        {"tasks": tasks}
    )

def create_documents(documents: list):
    """Creates or updates Document nodes in Neo4j from JSON data."""
    
    query = """
    UNWIND $documents AS document
    MERGE (d:Document {id: document.id})
    SET
        d.title = document.title,
        d.type = document.type,
        d.project_id = document.project_id,
        d.content = document.content
    """

    neo4j_client.execute_query(
        query,
        {"documents": documents}
    )
