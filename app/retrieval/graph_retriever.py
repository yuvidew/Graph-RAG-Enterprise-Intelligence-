from app.graph.neo4j_client import neo4j_client

class GraphRetriever:
    """Provides reusable functions for retrieving enterprise context from Neo4j."""

    def get_employee_by_name(self, name: str):
        """Finds an employee by name and returns basic employee information"""

        query = """
        MATCH (e:Employee)
        WHERE toLower(e.name) CONTAINS toLower($name)
        RETURN
            e.id AS id,
            e.name AS name,
            e.role AS role,
            e.email AS email
        LIMIT 10
        """

        result = neo4j_client.execute_query(
            query,
            {"name": name}
        )

        return result

    def get_employee_by_id(self, employee_id: str):
        """Retrieves basic details of a specific employee by ID."""

        query = """
        MATCH (e:Employee {id: $employee_id})

        RETURN
            e.id AS id,
            e.name AS name,
            e.role AS role,
            e.email AS email
        """

        result = neo4j_client.execute_query(
            query,
            {"employee_id": employee_id}
        )

        return result


    def get_employee_skills(self, employee_id: str):
        """Retrieves all skills associated with a specific employee."""

        query = """
        MATCH (e:Employee {id: $employee_id})
              -[:HAS_SKILL]->
              (s:Skill)

        RETURN
            e.name AS employee,
            s.id AS skill_id,
            s.name AS skill,
            s.category AS category
        ORDER BY s.name
        """

        result = neo4j_client.execute_query(
            query,
            {"employee_id": employee_id}
        )

        return result

    def get_employee_projects(self, employee_id: str):
        """Retrieves all projects assigned to a specific employee."""

        query = """
        MATCH (e:Employee {id: $employee_id})
              -[:WORKS_ON]->
              (p:Project)

        RETURN
            e.name AS employee,
            p.id AS project_id,
            p.name AS project,
            p.status AS status,
            p.category AS category
        ORDER BY p.name
        """

        result = neo4j_client.execute_query(
            query,
            {"employee_id": employee_id}
        )

        return result

    def get_project_team(self, project_id: str):
        """Retrieves all employees working on a specific project."""

        query = """
        MATCH (p:Project {id: $project_id})
              <-[:WORKS_ON]-
              (e:Employee)

        RETURN
            p.name AS project,
            e.id AS employee_id,
            e.name AS employee,
            e.role AS role
        ORDER BY e.name
        """

        result = neo4j_client.execute_query(
            query,
            {"project_id": project_id}
        )

        return result

    def get_project_customer(self, project_id: str):
        """Retrieves customers associated with a specific project."""

        query = """
        MATCH (p:Project {id: $project_id})
              -[:SERVES]->
              (c:Customer)

        RETURN
            p.name AS project,
            c.id AS customer_id,
            c.name AS customer,
            c.industry AS industry
        """

        result = neo4j_client.execute_query(
            query,
            {"project_id": project_id}
        )

        return result

    def get_employee_manager(self, employee_id: str):
        """Finds the manager that a specific employee reports to."""

        query = """
        MATCH (e:Employee {id: $employee_id})
              -[:REPORTS_TO]->
              (m:Employee)

        RETURN
            e.name AS employee,
            m.id AS manager_id,
            m.name AS manager,
            m.role AS manager_role
        """

        result = neo4j_client.execute_query(
            query,
            {"employee_id": employee_id}
        )

        return result

    def get_task_details(self, task_id: str):
        """Retrieves a task with its assigned employee and related project."""

        query = """
        MATCH (t:Task {id: $task_id})
        OPTIONAL MATCH (t)-[:ASSIGNED_TO]->(e:Employee)
        OPTIONAL MATCH (t)-[:BELONGS_TO]->(p:Project)

        RETURN
            t.id AS task_id,
            t.title AS title,
            t.description AS description,
            t.status AS status,
            t.priority AS priority,
            e.id AS employee_id,
            e.name AS employee,
            p.id AS project_id,
            p.name AS project
        """

        result = neo4j_client.execute_query(
            query,
            {"task_id": task_id}
        )

        return result

    def get_project_by_id(self, project_id: str):
        """Retrieves basic details of a specific project, including its company."""

        query = """
        MATCH (p:Project {id: $project_id})
        OPTIONAL MATCH (p)-[:BELONGS_TO]->(c:Company)

        RETURN
            p.id AS project_id,
            p.name AS project,
            p.status AS status,
            p.category AS category,
            c.id AS company_id,
            c.name AS company
        """

        result = neo4j_client.execute_query(
            query,
            {"project_id": project_id}
        )

        return result
    def get_project_tasks(self, project_id: str):
        """Retrieves all tasks belonging to a specific project."""

        query = """
        MATCH (t:Task)
              -[:BELONGS_TO]->
              (p:Project {id: $project_id})

        RETURN
            t.id AS task_id,
            t.title AS title,
            t.status AS status,
            t.priority AS priority
        ORDER BY t.title
        """

        result = neo4j_client.execute_query(
            query,
            {"project_id": project_id}
        )

        return result

    def get_customer_by_id(self, customer_id: str):
        """Retrieves basic details of a specific customer."""

        query = """
        MATCH (c:Customer {id: $customer_id})

        RETURN
            c.id AS customer_id,
            c.name AS customer,
            c.industry AS industry
        """

        result = neo4j_client.execute_query(
            query,
            {"customer_id": customer_id}
        )

        return result

    def get_customer_projects(self, customer_id: str):
        """Retrieves all projects serving a specific customer."""

        query = """
        MATCH (p:Project)
              -[:SERVES]->
              (c:Customer {id: $customer_id})

        RETURN
            p.id AS project_id,
            p.name AS project,
            p.status AS status
        ORDER BY p.name
        """

        result = neo4j_client.execute_query(
            query,
            {"customer_id": customer_id}
        )

        return result

    def get_department_by_id(self, department_id: str):
        """Retrieves basic details of a specific department, including its company."""

        query = """
        MATCH (d:Department {id: $department_id})
        OPTIONAL MATCH (c:Company)-[:HAS_DEPARTMENT]->(d)

        RETURN
            d.id AS department_id,
            d.name AS department,
            c.id AS company_id,
            c.name AS company
        """

        result = neo4j_client.execute_query(
            query,
            {"department_id": department_id}
        )

        return result

    def get_department_employees(self, department_id: str):
        """Retrieves all employees belonging to a specific department."""

        query = """
        MATCH (e:Employee)
              -[:BELONGS_TO]->
              (d:Department {id: $department_id})

        RETURN
            e.id AS employee_id,
            e.name AS employee,
            e.role AS role
        ORDER BY e.name
        """

        result = neo4j_client.execute_query(
            query,
            {"department_id": department_id}
        )

        return result   

    def get_company_by_id(self, company_id :str):
        """Retrieves basic details of a specific company."""

        query = """
        MATCH (c:Company {id: $company_id})

        RETURN
            c.id AS company_id,
            c.name AS company
        """

        result = neo4j_client.execute_query(
            query,
            {"company_id": company_id}
        )

        return result

    def get_company_departments(self, company_id: str):
        """Retrieves all departments belonging to a specific company."""

        query = """
        MATCH (c:Company {id: $company_id})
              -[:HAS_DEPARTMENT]->
              (d:Department)

        RETURN
            d.id AS department_id,
            d.name AS department
        ORDER BY d.name
        """

        result = neo4j_client.execute_query(
            query,
            {"company_id": company_id}
        )

        return result

    def get_company_projects(self, company_id: str):
        """Retrieves all projects belonging to a specific company."""

        query = """
        MATCH (p:Project)
              -[:BELONGS_TO]->
              (c:Company {id: $company_id})

        RETURN
            p.id AS project_id,
            p.name AS project,
            p.status AS status
        ORDER BY p.name
        """

        result = neo4j_client.execute_query(
            query,
            {"company_id": company_id}
        )

        return result

    def get_document_by_id(self, document_id: str):
        """Retrieves a document along with its related project."""

        query = """
        MATCH (doc:Document {id: $document_id})
        OPTIONAL MATCH (doc)-[:DOCUMENTS]->(p:Project)

        RETURN
            doc.id AS document_id,
            doc.title AS title,
            doc.type AS type,
            p.id AS project_id,
            p.name AS project
        """

        result = neo4j_client.execute_query(
            query,
            {"document_id": document_id}
        )

        return result

    def get_skill_by_id(self, skill_id: str):
        """Retrieves basic details of a specific skill."""

        query = """
        MATCH (s:Skill {id: $skill_id})

        RETURN
            s.id AS skill_id,
            s.name AS skill,
            s.category AS category
        """

        result = neo4j_client.execute_query(
            query,
            {"skill_id": skill_id}
        )

        return result

    def get_skill_employees(self, skill_id: str):
        """Retrieves all employees who have a specific skill."""

        query = """
        MATCH (e:Employee)
              -[:HAS_SKILL]->
              (s:Skill {id: $skill_id})

        RETURN
            e.id AS employee_id,
            e.name AS employee,
            e.role AS role
        ORDER BY e.name
        """

        result = neo4j_client.execute_query(
            query,
            {"skill_id": skill_id}
        )

        return result

    def get_project_by_name(self, name: str):
        """Find a project by name."""

        query = """
        MATCH (p:Project)
        WHERE toLower(p.name) CONTAINS toLower($name)
        RETURN
            p.id AS id,
            p.name AS name,
            p.status AS status
        LIMIT 10
        """

        result = neo4j_client.execute_query(
            query,
            {"name": name}
        )

        return result

    def get_customer_by_name(self, name: str):
            """Find a customer by name."""
    
            query = """
            MATCH (p:Customer)
            WHERE toLower(p.name) CONTAINS toLower($name)
            RETURN
                p.id AS id,
                p.name AS name,
                p.status AS status
            LIMIT 10
            """
    
            result = neo4j_client.execute_query(
                query,
                {"name": name}
            )
    
            return result

    def get_department_by_name(self, name: str):
        """Find a department by name."""

        query = """
        MATCH (d:Department)
        WHERE toLower(d.name) CONTAINS toLower($name)
        RETURN
            d.id AS id,
            d.name AS name
        LIMIT 10
        """
        result = neo4j_client.execute_query(
            query,
            {"name": name}
        )

        return result

    def get_company_by_name(self, name: str):
        """Finds a company by name"""

        query = """
        MATCH (c:Company)
        WHERE toLower(c.name) CONTAINS toLower($name)
        RETURN
            c.id AS id,
            c.name AS name
        LIMIT 10
        """

        result = neo4j_client.execute_query(
            query,
            {"name": name}
        )

        return result

    def get_skill_by_name(self, name: str):
        """Finds a skill by name"""

        query = """
        MATCH (s:Skill)
        WHERE toLower(s.name) CONTAINS toLower($name)
        RETURN
            s.id AS id,
            s.name AS name,
            s.category AS category
        LIMIT 10
        """

        result = neo4j_client.execute_query(
            query,
            {"name": name}
        )

        return result

    def get_document_by_title(self, title: str):
        """Finds a document by title."""

        query = """
        MATCH (doc:Document)
        WHERE toLower(doc.title) CONTAINS toLower($title)
        RETURN
            doc.id AS id,
            doc.title AS title
        LIMIT 10
        """

        result = neo4j_client.execute_query(
            query,
            {"title": title}
        )

        return result
