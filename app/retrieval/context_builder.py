from app.retrieval.graph_retriever import GraphRetriever

class GraphContextBuilder:
    """Builds structured enterprise context from Neo4j retrieval results."""

    def __init__(self):
        self.retriever = GraphRetriever()

    def build_employee_context(self, employee_id: str) -> dict:
        """Builds a complete knowledge context for a specific employee."""

        employee = self.retriever.get_employee_by_id(employee_id)
        skills = self.retriever.get_employee_skills(employee_id)
        projects = self.retriever.get_employee_projects(employee_id)
        manager = self.retriever.get_employee_manager(employee_id)

        project_context = []

        for project in projects:
            project_id = project["project_id"]

            team = self.retriever.get_project_team(project_id)
            customers = self.retriever.get_project_customer(project_id)

            project_context.append(
                {
                    "project": project,
                    "team": team,
                    "customers": customers,
                }
            )

        context = {
            "employee_id": employee_id,
            "employee": employee,
            "skills": skills,
            "projects": project_context,
            "manager": manager,
        }

        return context

    def build_project_context(self, project_id: str) -> dict:
        """Builds a complete knowledge context for a specific project."""

        project = self.retriever.get_project_by_id(project_id)
        team = self.retriever.get_project_team(project_id)
        customers = self.retriever.get_project_customer(project_id)
        tasks = self.retriever.get_project_tasks(project_id)

        context = {
            "project_id": project_id,
            "project": project,
            "team": team,
            "customers": customers,
            "tasks": tasks,
        }

        return context

    def build_task_context(self, task_id: str) -> dict:
        """Builds a complete knowledge context for a specific task."""

        task = self.retriever.get_task_details(task_id)

        context = {
            "task_id": task_id,
            "task": task,
        }

        return context

    def build_customer_context(self, customer_id: str) -> dict:
        """Builds a complete knowledge context for a specific customer."""

        customer = self.retriever.get_customer_by_id(customer_id)
        projects = self.retriever.get_customer_projects(customer_id)

        context = {
            "customer_id": customer_id,
            "customer": customer,
            "projects": projects,
        }

        return context

    def build_department_context(self, department_id: str) -> dict:
        """Builds a complete knowledge context for a specific department."""

        department = self.retriever.get_department_by_id(department_id)
        employees = self.retriever.get_department_employees(department_id)

        context = {
            "department_id": department_id,
            "department": department,
            "employees": employees,
        }

        return context

    def build_company_context(self, company_id: str) -> dict:
        """Builds a complete knowledge context for a specific company."""

        company = self.retriever.get_company_by_id(company_id)
        departments = self.retriever.get_company_departments(company_id)
        projects = self.retriever.get_company_projects(company_id)

        context = {
            "company_id": company_id,
            "company": company,
            "departments": departments,
            "projects": projects,
        }

        return context

    def build_document_context(self, document_id: str) -> dict:
        """Builds a complete knowledge context for a specific document."""

        document = self.retriever.get_document_by_id(document_id)

        context = {
            "document_id": document_id,
            "document": document,
        }

        return context

    def build_skill_content(self, skill_id: str) -> dict:
        """Builds a complete knowledge context for a specific skill."""

        skill = self.retriever.get_skill_by_id(skill_id)
        employees = self.retriever.get_skill_employees(skill_id)

        context = {
            "skill_id": skill_id,
            "skill": skill,
            "employees": employees,
        }

        return context
