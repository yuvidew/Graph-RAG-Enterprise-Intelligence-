def format_employee_context(context: dict) -> str:
    """Converts the employee context dict into a readable text block for the LLM prompt."""

    lines = []

    # ---Employes basic info ---
    employee_id =context.get("employee_id")
    employee = context.get("employee")

    if employee:
        e = employee[0]
        lines.append(f"Employee: {e['name']} (ID: {employee_id}, Role : {e['role']})")
    else:
        lines.append(f"Employee ID: {employee_id}")

    #  ---Manage---
    manager = context.get("manager")
    if manager:
        m = manager[0] # manager query returns a list
        lines.append(f"Manager: {m['manager']} ({m['manager_role']})")
    else:
        lines.append("Manager: None")

    # ---Skills---
    skills = context.get("skills", [])

    if skills:
        lines.append("\nSkills:")
        for s in skills:
            lines.append(f"- {s['skill']} ({s['category']})")
    else:
        lines.append("\nSkills: None")

    #  ---Projects---
    projects = context.get("projects", [])
    if projects:
        lines.append("\nProjects:")
        for p in projects:
            project = p['project']
            team = p["team"]
            customers = p["customers"]

            lines.append(f"- {project['project']} (status: {project['status']})")

            if team:
                team_names = ", ".join(t["employee"] for t in team)
                lines.append(f"  Team: {team_names}")
            if customers:
                customer_names = ", ".join(c["customer"] for c in customers)
                lines.append(f"  Customers: {customer_names}")

    else:
        lines.append("\nProjects: None")

    return "\n".join(lines)

def format_project_context(context: dict) -> str:
    """Converts the project context dict into a readable text block for the LLM prompt."""

    lines = []

    project = context.get("project")

    if project: 
        p = project[0]
        lines.append(f"Project: {p['project']} (status: {p['status']}, category: {p['category']})")
        lines.append(f"Company: {p['company']}")
    else:
        lines.append("Project: Not found")

    team = context.get("team", [])
    if team: 
        lines.append("\nTeam:")
        for member in team:
            lines.append(f"- {member['employee']} ({member['role']})")
    else: 
        lines.append("\nTeam: None")


    customers = context.get("customers", [])
    if customers: 
        lines.append("\nCustomers:")
        for c in customers:
            lines.append(f"- {c['customer']} ({c['industry']})")
    else:
        lines.append("\nCustomers: None")

    tasks = context.get("tasks", [])
    if tasks:
        lines.append("\nTasks:")
        for t in tasks:
            lines.append(f"- {t['title']} (status: {t['status']}, priority: {t['priority']})")
    else:
        lines.append("\nTasks: None")

    return "\n".join(lines)

def format_task_context(context: dict) -> str:
    """Converts the task context dict into a readable text block for the LLM prompt."""

    lines = []

    task = context.get("task")
    if task: 
        t = task[0]
        lines.append(f"Task: {t['title']}")
        lines.append(f"Description: {t['description']}")
        lines.append(f"Status: {t['status']}, Priority: {t['priority']}")
        lines.append(f"Assigned to: {t['employee']}")
        lines.append(f"Project: {t['project']}")
    else:
        lines.append("Task: Not found")

    return "\n".join(lines)

def format_customer_context(context: dict) -> str:
    """Converts the customer context dict into a readable text block for the LLM prompt."""

    lines = []

    customer = context.get("customer")
    if customer:
        c = customer[0]
        lines.append(f"Customer: {c['customer']} (industry: {c['industry']})")
    else:
        lines.append("Customer: Not found")

    projects = context.get("projects", [])
    if projects:
        lines.append("\nProjects:")
        for p in projects:
            lines.append(f"- {p['project']} (status: {p['status']})")
    else:
        lines.append("\nProjects: None")

    return "\n".join(lines)

def format_department_context(context: dict) -> str:
    """Converts the department context dict into a readable text block for the LLM prompt."""

    lines = []

    department = context.get("department")
    if department:
        d = department[0]
        lines.append(f"Department: {d['department']}")
        lines.append(f"Company: {d['company']}")
    else:
        lines.append("Department: Not found")

    employees = context.get("employees", [])
    if employees:
        lines.append("\nEmployees:")
        for e in employees:
            lines.append(f"- {e['employee']} ({e['role']})")
    else:
        lines.append("\nEmployees: None")

    return "\n".join(lines)

def format_company_context(context: dict) -> str:
    """Converts the company context dict into a readable text block for the LLM prompt."""

    lines = []

    company = context.get("company")
    if company:
        c = company[0]
        lines.append(f"Company: {c['company']}")
    else:
        lines.append("Company: Not found")

    departments = context.get("departments", [])
    if departments:
        lines.append("\nDepartments:")
        for d in departments:
            lines.append(f"- {d['department']}")
    else:
        lines.append("\nDepartments: None")

    projects = context.get("projects", [])
    if projects:
        lines.append("\nProjects:")
        for p in projects:
            lines.append(f"- {p['project']} (status: {p['status']})")
    else:
        lines.append("\nProjects: None")

    return "\n".join(lines)

def format_document_context(context: dict) -> str:
    """Converts the document context dict into a readable text block for the LLM prompt."""

    lines = []

    document = context.get("document")
    if document:
        d = document[0]
        lines.append(f"Document: {d['title']} (type: {d['type']})")
        lines.append(f"Related Project: {d['project']}")
    else:
        lines.append("Document: Not found")

    return "\n".join(lines)

def format_skill_context(context: dict) -> str:
    """Converts the skill context dict into a readable text block for the LLM prompt."""
    lines =[]

    skill = context.get("skill")
    if skill:
        s = skill[0]
        lines.append(f"Skill: {s['skill']} (category: {s['category']})")
    else: 
        lines.append("Skill: Not found")

    employees = context.get("employees", [])

    if employees:
        lines.append("\nEmployees with this skill:")
        for e in employees:
            lines.append(f"- {e['employee']} ({e['role']})")
    else:
        lines.append("\nEmployees: None")


    return "\n".join(lines)
