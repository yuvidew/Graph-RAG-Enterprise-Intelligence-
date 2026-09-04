SCHEMA_QUERIES = [
    """
    CREATE CONSTRAINT company_id_unique IF NOT EXISTS
    FOR (c:Company)
    REQUIRE c.id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT department_id_unique IF NOT EXISTS
    FOR (d:Department)
    REQUIRE d.id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT employee_id_unique IF NOT EXISTS
    FOR (e:Employee)
    REQUIRE e.id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT skill_id_unique IF NOT EXISTS
    FOR (s:Skill)
    REQUIRE s.id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT project_id_unique IF NOT EXISTS
    FOR (p:Project)
    REQUIRE p.id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT task_id_unique IF NOT EXISTS
    FOR (t:Task)
    REQUIRE t.id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT customer_id_unique IF NOT EXISTS
    FOR (c:Customer)
    REQUIRE c.id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT document_id_unique IF NOT EXISTS
    FOR (d:Document)
    REQUIRE d.id IS UNIQUE
    """,
]
