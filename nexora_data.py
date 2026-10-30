import random
import sqlite3
from datetime import date, datetime, timedelta


COMPANY = {
    "name": "NEXORA TECHNOLOGIES",
    "tagline": "Engineering Tomorrow Through Intelligent Innovation.",
    "industry": "Technology and IT Services",
    "business_model": "Software development, enterprise solutions, cloud services, AI and data analytics",
    "headquarters": "Bengaluru, India",
    "workforce_target": 850,
}

DEPARTMENT_DATA = [
    ("Engineering", 220, 32, "Product engineering, enterprise software and quality engineering.", ["Python", "Java", "TypeScript", "React", "API Design", "Agile"]),
    ("Data & Analytics", 80, 14, "Data platforms, applied AI, business intelligence and analytics.", ["SQL", "Python", "Machine Learning", "Power BI", "Statistics", "Data Engineering"]),
    ("Product Management", 55, 8, "Product strategy, discovery, delivery and design.", ["Product Strategy", "Roadmapping", "Agile", "UX Research", "Jira"]),
    ("Human Resources", 35, 5, "People operations, talent acquisition and employee experience.", ["Talent Acquisition", "People Analytics", "Employee Relations", "HRIS"]),
    ("Finance", 45, 5, "Financial planning, accounting, procurement and business control.", ["Financial Analysis", "Accounting", "Forecasting", "Excel", "Compliance"]),
    ("Marketing", 55, 7, "Corporate marketing, demand generation and brand.", ["Marketing Analytics", "Content Strategy", "SEO", "Campaign Management"]),
    ("Sales", 80, 12, "Enterprise sales, account growth and customer partnerships.", ["Enterprise Sales", "CRM", "Negotiation", "Account Management"]),
    ("Cloud & Infrastructure", 100, 14, "Cloud platforms, SRE, IT infrastructure and operations.", ["AWS", "Azure", "Kubernetes", "Linux", "DevOps", "SRE"]),
    ("Cybersecurity", 70, 10, "Security engineering, governance, risk and incident response.", ["Cybersecurity", "Cloud Security", "SIEM", "Incident Response", "Compliance"]),
    ("Business Operations", 110, 13, "Business operations, delivery excellence and corporate services.", ["Project Management", "Process Improvement", "Business Analysis", "Communication", "Excel"]),
]

LOCATION_DATA = [
    ("Bengaluru", "Karnataka", "Headquarters"),
    ("Chennai", "Tamil Nadu", "Delivery office"),
    ("Hyderabad", "Telangana", "Technology office"),
    ("Pune", "Maharashtra", "Enterprise solutions office"),
]

DEMO_JOBS = [
    ("Senior Software Engineer", "Engineering", "Build secure, scalable enterprise applications and coach engineering peers.", "Python, API Design, SQL, Agile", 5, 24, 34, 3),
    ("Software Engineer", "Engineering", "Deliver tested backend and full-stack features for Nexora client platforms.", "Java, SQL, Agile", 2, 12, 20, 4),
    ("Python Developer", "Engineering", "Develop reliable Python services and integrations for Nexora enterprise platforms.", "Python, SQL, API Design", 2, 14, 22, 2),
    ("Frontend Engineer", "Engineering", "Build accessible, responsive product experiences with modern web technologies.", "TypeScript, React, UX Research", 3, 16, 24, 2),
    ("QA Automation Engineer", "Engineering", "Improve release quality through automated test design and CI pipelines.", "Python, API Design, Jira", 3, 14, 22, 2),
    ("Data Analyst", "Data & Analytics", "Translate enterprise data into governed dashboards and practical insights.", "SQL, Power BI, Statistics", 2, 12, 19, 3),
    ("Machine Learning Engineer", "Data & Analytics", "Develop and evaluate applied machine-learning services with product teams.", "Python, Machine Learning, SQL", 4, 22, 32, 2),
    ("Data Engineer", "Data & Analytics", "Build reliable, documented data pipelines and curated analytics models.", "SQL, Python, Data Engineering", 3, 18, 27, 2),
    ("Product Manager", "Product Management", "Set product direction and align discovery, delivery and customer outcomes.", "Product Strategy, Roadmapping, Agile", 5, 26, 38, 1),
    ("Technical Recruiter", "Human Resources", "Partner with engineering leaders to deliver structured, fair hiring processes.", "Talent Acquisition, Communication, People Analytics", 3, 12, 20, 2),
    ("Financial Analyst", "Finance", "Support planning cycles, variance analysis and business decision support.", "Financial Analysis, Forecasting, Excel", 2, 10, 17, 1),
    ("Digital Marketing Manager", "Marketing", "Plan measurable campaigns for Nexora's enterprise and cloud services.", "Marketing Analytics, Campaign Management, SEO", 5, 20, 30, 1),
    ("Enterprise Account Executive", "Sales", "Build trusted client relationships and qualify enterprise solution opportunities.", "Enterprise Sales, CRM, Negotiation", 5, 24, 40, 3),
    ("Cloud Platform Engineer", "Cloud & Infrastructure", "Operate resilient cloud foundations and improve deployment automation.", "AWS, Kubernetes, DevOps", 4, 20, 30, 3),
    ("Site Reliability Engineer", "Cloud & Infrastructure", "Improve service reliability, observability and incident readiness.", "SRE, Linux, Kubernetes", 4, 20, 30, 2),
    ("Security Analyst", "Cybersecurity", "Monitor security signals, investigate incidents and strengthen controls.", "Cybersecurity, SIEM, Incident Response", 3, 17, 26, 2),
    ("Business Operations Analyst", "Business Operations", "Map operating processes and coordinate measurable service improvements.", "Business Analysis, Process Improvement, Excel", 2, 11, 18, 2),
    ("Delivery Project Manager", "Business Operations", "Coordinate enterprise delivery plans, risks and stakeholder communication.", "Project Management, Communication, Agile", 5, 21, 32, 2),
    ("People Analytics Specialist", "Human Resources", "Create trusted workforce reporting and support evidence-led people programs.", "People Analytics, SQL, Power BI", 3, 15, 23, 1),
]

TEAM_NAMES = {
    "Engineering": ["Platform Engineering", "Enterprise Applications", "Digital Products", "Quality Engineering", "Developer Experience"],
    "Data & Analytics": ["Data Engineering", "Business Intelligence", "Applied AI", "Data Governance", "Customer Analytics"],
    "Product Management": ["Enterprise Products", "Cloud Products", "Product Design", "Product Operations", "Customer Discovery"],
    "Human Resources": ["Talent Acquisition", "People Operations", "Learning & Development", "People Analytics", "Employee Experience"],
    "Finance": ["Financial Planning", "Accounting", "Commercial Finance", "Procurement", "Risk & Compliance"],
    "Marketing": ["Brand & Content", "Demand Generation", "Digital Marketing", "Product Marketing", "Marketing Operations"],
    "Sales": ["Enterprise Accounts", "Cloud Sales", "Strategic Partnerships", "Inside Sales", "Sales Operations"],
    "Cloud & Infrastructure": ["Cloud Foundations", "Site Reliability", "Infrastructure Operations", "DevOps Enablement", "Cloud FinOps"],
    "Cybersecurity": ["Security Operations", "Cloud Security", "Application Security", "Governance & Risk", "Security Engineering"],
    "Business Operations": ["Enterprise Delivery", "Business Excellence", "Client Operations", "Workplace Services", "Program Management"],
}

FIRST_NAMES = [
    "Aadhya", "Aarav", "Aditi", "Aditya", "Akash", "Amara", "Ananya", "Arjun", "Avani",
    "Dev", "Diya", "Esha", "Gaurav", "Ira", "Ishaan", "Kabir", "Kavya", "Kiran",
    "Krishna", "Maya", "Meera", "Neel", "Nisha", "Nikhil", "Pooja", "Pranav",
    "Rhea", "Rohan", "Sana", "Sanjay", "Shaan", "Shreya", "Tara", "Varun", "Vihaan",
]
LAST_NAMES = [
    "Agarwal", "Bansal", "Chandra", "Desai", "Iyer", "Jain", "Kapoor", "Khanna",
    "Kulkarni", "Menon", "Mehta", "Mishra", "Nair", "Pillai", "Rao", "Reddy",
    "Shah", "Sharma", "Singh", "Srinivasan", "Thomas", "Varma", "Verma", "Patel",
    "Joshi", "Gupta", "Das", "Kumar", "Fernandes", "Banerjee", "Shetty", "Malhotra",
]

LEARNING_RESOURCES = [
    ("SQL Foundations", "DataCamp", "Structured learning path for SQL querying and data modeling.", "SQL"),
    ("Microsoft Power BI Data Analyst", "Microsoft Learn", "Free learning modules for Power BI data preparation and reporting.", "Power BI"),
    ("AWS Skill Builder", "AWS", "Official digital training for cloud infrastructure and AWS services.", "AWS"),
    ("Kubernetes Basics", "Linux Foundation", "Introductory lessons for container orchestration concepts.", "Kubernetes"),
    ("Python for Everybody", "University of Michigan", "Open course covering Python programming foundations.", "Python"),
    ("Google Project Management", "Coursera", "Project planning, delivery and stakeholder skills.", "Project Management"),
    ("Microsoft Security Learning", "Microsoft Learn", "Security operations and cloud security learning paths.", "Cybersecurity"),
    ("Product Management Fundamentals", "Atlassian University", "Product discovery, roadmapping and agile delivery resources.", "Product Strategy"),
    ("Excel Skills for Business", "Macquarie University", "Practice-focused spreadsheet analysis and reporting.", "Excel"),
    ("People Analytics", "AIHR", "People data and workforce analytics learning resources.", "People Analytics"),
]


def _ensure_column(conn, table, column, definition):
    columns = {row["name"] for row in conn.execute(f"PRAGMA table_info({table})")}
    if column not in columns:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")


def ensure_schema(conn):
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS company (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        tagline TEXT NOT NULL,
        industry TEXT NOT NULL,
        business_model TEXT NOT NULL,
        headquarters TEXT NOT NULL,
        workforce_target INTEGER NOT NULL,
        is_synthetic INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS locations (
        id INTEGER PRIMARY KEY,
        company_id INTEGER NOT NULL REFERENCES company(id),
        name TEXT NOT NULL,
        state TEXT NOT NULL,
        office_type TEXT NOT NULL,
        is_synthetic INTEGER NOT NULL DEFAULT 1,
        UNIQUE(company_id, name)
    );
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY,
        company_id INTEGER NOT NULL REFERENCES company(id),
        name TEXT NOT NULL,
        description TEXT NOT NULL DEFAULT '',
        head_employee_id INTEGER,
        hiring_target INTEGER NOT NULL DEFAULT 0,
        is_synthetic INTEGER NOT NULL DEFAULT 1,
        UNIQUE(company_id, name)
    );
    CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY,
        department_id INTEGER NOT NULL REFERENCES departments(id),
        name TEXT NOT NULL,
        manager_employee_id INTEGER,
        team_lead_employee_id INTEGER,
        is_synthetic INTEGER NOT NULL DEFAULT 1,
        UNIQUE(department_id, name)
    );
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        company_id INTEGER NOT NULL REFERENCES company(id),
        employee_code TEXT NOT NULL UNIQUE,
        full_name TEXT NOT NULL,
        department_id INTEGER NOT NULL REFERENCES departments(id),
        team_id INTEGER REFERENCES teams(id),
        manager_id INTEGER REFERENCES employees(id),
        designation TEXT NOT NULL,
        experience_years REAL NOT NULL DEFAULT 0,
        location_id INTEGER REFERENCES locations(id),
        joined_on TEXT NOT NULL,
        separated_on TEXT,
        employment_status TEXT NOT NULL DEFAULT 'Active',
        certifications TEXT NOT NULL DEFAULT '',
        is_synthetic INTEGER NOT NULL DEFAULT 1
    );
    CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        skill_group TEXT NOT NULL DEFAULT 'Business'
    );
    CREATE TABLE IF NOT EXISTS employee_skills (
        employee_id INTEGER NOT NULL REFERENCES employees(id),
        skill_id INTEGER NOT NULL REFERENCES skills(id),
        proficiency INTEGER NOT NULL DEFAULT 3 CHECK(proficiency BETWEEN 1 AND 5),
        PRIMARY KEY(employee_id, skill_id)
    );
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY,
        company_id INTEGER NOT NULL REFERENCES company(id),
        department_id INTEGER NOT NULL REFERENCES departments(id),
        team_id INTEGER REFERENCES teams(id),
        name TEXT NOT NULL,
        client_name TEXT NOT NULL,
        description TEXT NOT NULL DEFAULT '',
        required_skills TEXT NOT NULL DEFAULT '',
        status TEXT NOT NULL DEFAULT 'Active',
        priority TEXT NOT NULL DEFAULT 'Medium',
        start_date TEXT NOT NULL,
        target_end_date TEXT NOT NULL,
        is_synthetic INTEGER NOT NULL DEFAULT 1,
        UNIQUE(company_id, name)
    );
    CREATE TABLE IF NOT EXISTS project_allocations (
        employee_id INTEGER NOT NULL REFERENCES employees(id),
        project_id INTEGER NOT NULL REFERENCES projects(id),
        allocation_pct REAL NOT NULL CHECK(allocation_pct BETWEEN 0 AND 100),
        allocated_at TEXT NOT NULL,
        PRIMARY KEY(employee_id, project_id)
    );
    CREATE TABLE IF NOT EXISTS interviews (
        id INTEGER PRIMARY KEY,
        application_id INTEGER NOT NULL REFERENCES applications(id),
        interviewer_employee_id INTEGER REFERENCES employees(id),
        scheduled_at TEXT NOT NULL,
        interview_type TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Scheduled',
        notes TEXT NOT NULL DEFAULT '',
        is_synthetic INTEGER NOT NULL DEFAULT 1
    );
    CREATE TABLE IF NOT EXISTS recruitment_costs (
        application_id INTEGER PRIMARY KEY REFERENCES applications(id),
        source TEXT NOT NULL,
        advertising_cost REAL NOT NULL DEFAULT 0,
        recruiter_hours REAL NOT NULL DEFAULT 0,
        hourly_rate REAL NOT NULL DEFAULT 0,
        is_synthetic INTEGER NOT NULL DEFAULT 1
    );
    CREATE TABLE IF NOT EXISTS talent_pool (
        candidate_id INTEGER PRIMARY KEY REFERENCES candidates(id),
        consent_status TEXT NOT NULL CHECK(consent_status IN ('Granted','Withdrawn')),
        consented_at TEXT NOT NULL,
        source_application_id INTEGER REFERENCES applications(id),
        notes TEXT NOT NULL DEFAULT ''
    );
    CREATE TABLE IF NOT EXISTS talent_recommendations (
        id INTEGER PRIMARY KEY,
        candidate_id INTEGER NOT NULL REFERENCES candidates(id),
        job_id INTEGER NOT NULL REFERENCES jobs(id),
        match_score REAL NOT NULL,
        missing_skills TEXT NOT NULL DEFAULT '',
        status TEXT NOT NULL DEFAULT 'Recommended',
        created_at TEXT NOT NULL,
        UNIQUE(candidate_id, job_id)
    );
    CREATE TABLE IF NOT EXISTS teamfit_assessments (
        id INTEGER PRIMARY KEY,
        application_id INTEGER NOT NULL REFERENCES applications(id),
        team_id INTEGER NOT NULL REFERENCES teams(id),
        fit_score REAL NOT NULL,
        skill_coverage_before REAL NOT NULL,
        skill_coverage_after REAL NOT NULL,
        capacity_headroom REAL NOT NULL,
        rationale TEXT NOT NULL,
        assessed_at TEXT NOT NULL,
        UNIQUE(application_id, team_id)
    );
    CREATE TABLE IF NOT EXISTS team_allocations (
        id INTEGER PRIMARY KEY,
        application_id INTEGER NOT NULL REFERENCES applications(id),
        team_id INTEGER NOT NULL REFERENCES teams(id),
        project_id INTEGER REFERENCES projects(id),
        allocated_by_employee_id INTEGER REFERENCES employees(id),
        approved_by_employee_id INTEGER REFERENCES employees(id),
        approved_at TEXT,
        allocation_pct REAL NOT NULL DEFAULT 100,
        status TEXT NOT NULL DEFAULT 'Proposed',
        created_at TEXT NOT NULL,
        UNIQUE(application_id)
    );
    CREATE TABLE IF NOT EXISTS notification_settings (
        setting_key TEXT PRIMARY KEY,
        setting_value TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS learning_resources(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        provider TEXT NOT NULL,
        description TEXT NOT NULL,
        skill_name TEXT NOT NULL,
        resource_url TEXT NOT NULL DEFAULT '',
        is_synthetic INTEGER NOT NULL DEFAULT 1,
        UNIQUE(title,provider)
    );
    CREATE TABLE IF NOT EXISTS message_drafts (
        id INTEGER PRIMARY KEY,
        candidate_id INTEGER REFERENCES candidates(id),
        recipient TEXT NOT NULL,
        subject TEXT NOT NULL,
        body TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Draft',
        approved_by_employee_id INTEGER REFERENCES employees(id),
        approved_at TEXT,
        created_at TEXT NOT NULL
    );
    """)

    job_columns = {
        "department_id": "INTEGER REFERENCES departments(id)",
        "location_id": "INTEGER REFERENCES locations(id)",
        "salary_min_lpa": "REAL NOT NULL DEFAULT 0",
        "salary_max_lpa": "REAL NOT NULL DEFAULT 0",
        "vacancies": "INTEGER NOT NULL DEFAULT 1",
        "is_synthetic": "INTEGER NOT NULL DEFAULT 0",
    }
    for column, definition in job_columns.items():
        _ensure_column(conn, "jobs", column, definition)
    candidate_columns = {
        "project_experience": "TEXT NOT NULL DEFAULT ''",
        "certifications": "TEXT NOT NULL DEFAULT ''",
        "talent_consent": "INTEGER NOT NULL DEFAULT 0",
        "is_synthetic": "INTEGER NOT NULL DEFAULT 0",
    }
    for column, definition in candidate_columns.items():
        _ensure_column(conn, "candidates", column, definition)
    _ensure_column(conn, "applications", "is_synthetic", "INTEGER NOT NULL DEFAULT 0")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_employees_department ON employees(department_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_employees_team ON employees(team_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_projects_department ON projects(department_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_interviews_schedule ON interviews(scheduled_at)")


def _rows(conn, query, parameters=()):
    return conn.execute(query, parameters).fetchall()


def _seed_employee_directory(conn, company_id, department_ids, location_ids, today):
    existing = conn.execute(
        "SELECT COUNT(*) FROM employees WHERE company_id=? AND is_synthetic=1", (company_id,)
    ).fetchone()[0]
    if existing:
        return

    counts = {name: count for name, count, _, _, _ in DEPARTMENT_DATA}
    team_ids = {}
    for department, _, _, _, _ in DEPARTMENT_DATA:
        for team_name in TEAM_NAMES[department]:
            cursor = conn.execute(
                "INSERT INTO teams(department_id,name,is_synthetic) VALUES(?,?,1)",
                (department_ids[department], team_name),
            )
            team_ids[(department, team_name)] = cursor.lastrowid

    department_head_ids = {}
    department_manager_ids = {}
    team_lead_ids = {}
    employee_index = 0

    def create_employee(department, designation, manager_id, team_id=None, join_date=None, status="Active"):
        nonlocal employee_index
        employee_index += 1
        first = FIRST_NAMES[(employee_index - 1) % len(FIRST_NAMES)]
        last = LAST_NAMES[((employee_index - 1) // len(FIRST_NAMES)) % len(LAST_NAMES)]
        name = f"{first} {last}"
        joined = join_date or (today - timedelta(days=180 + ((employee_index * 37) % 3100)))
        location_id = location_ids[LOCATION_DATA[(employee_index * 7) % len(LOCATION_DATA)][0]]
        separated_on = (today - timedelta(days=30 + employee_index % 320)) if status == "Separated" else None
        cursor = conn.execute(
            """INSERT INTO employees(
                company_id,employee_code,full_name,department_id,team_id,manager_id,
                designation,experience_years,location_id,joined_on,separated_on,
                employment_status,certifications,is_synthetic
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,1)""",
            (
                company_id, f"NX-{employee_index:04d}", name, department_ids[department],
                team_id, manager_id, designation, round(1 + ((employee_index * 7) % 140) / 10, 1),
                location_id, joined.isoformat(), separated_on.isoformat() if separated_on else None,
                status, "Cloud Practitioner" if employee_index % 13 == 0 else "",
            ),
        )
        return cursor.lastrowid

    ceo_id = create_employee("Business Operations", "Chief Executive Officer", None, join_date=date(2017, 1, 9))
    executives = {
        "Engineering": create_employee("Engineering", "Chief Technology Officer", ceo_id, join_date=date(2017, 3, 6)),
        "Finance": create_employee("Finance", "Chief Financial Officer", ceo_id, join_date=date(2017, 2, 13)),
        "Business Operations": create_employee("Business Operations", "Chief Operating Officer", ceo_id, join_date=date(2017, 2, 20)),
    }
    for department, _, _, _, _ in DEPARTMENT_DATA:
        executive = executives["Engineering"] if department in (
            "Engineering", "Data & Analytics", "Product Management", "Cloud & Infrastructure", "Cybersecurity"
        ) else executives["Finance"] if department == "Finance" else executives["Business Operations"]
        head_designation = f"{department} Department Head"
        head_id = create_employee(department, head_designation, executive)
        department_head_ids[department] = head_id

    for department, _, _, _, _ in DEPARTMENT_DATA:
        department_manager_ids[department] = [
            create_employee(department, "Senior Manager", department_head_ids[department])
            for _ in range(3)
        ]
        team_lead_ids[department] = []
        for index, team_name in enumerate(TEAM_NAMES[department]):
            team_id = team_ids[(department, team_name)]
            manager_id = department_manager_ids[department][index % 3]
            lead_id = create_employee(department, "Team Lead", manager_id, team_id=team_id)
            team_lead_ids[department].append(lead_id)
            conn.execute(
                "UPDATE teams SET manager_employee_id=?,team_lead_employee_id=? WHERE id=?",
                (manager_id, lead_id, team_id),
            )

    conn.execute(
        "UPDATE departments SET head_employee_id=? WHERE id=?",
        (department_head_ids["Business Operations"], department_ids["Business Operations"]),
    )
    for department, head_id in department_head_ids.items():
        conn.execute(
            "UPDATE departments SET head_employee_id=? WHERE id=?",
            (head_id, department_ids[department]),
        )

    created_by_department = {name: 0 for name in counts}
    created_by_department["Business Operations"] += 1
    created_by_department["Engineering"] += 1
    created_by_department["Finance"] += 1
    created_by_department["Business Operations"] += 1
    for department in counts:
        created_by_department[department] += 1
        created_by_department[department] += 3
        created_by_department[department] += len(TEAM_NAMES[department])

    remaining = {
        department: counts[department] - created_by_department[department]
        for department in counts
    }
    for department, remaining_count in remaining.items():
        for index in range(remaining_count):
            team_index = index % len(TEAM_NAMES[department])
            team_id = team_ids[(department, TEAM_NAMES[department][team_index])]
            manager_id = team_lead_ids[department][team_index]
            if index < 5 and department == "Engineering":
                joined = date(today.year, today.month, min(index + 1, today.day))
            else:
                joined = today - timedelta(days=45 + ((employee_index + index * 29) % 3200))
            status = "On Leave" if (employee_index + index) % 67 == 0 else (
                "Separated" if (employee_index + index) % 97 == 0 else "Active"
            )
            create_employee(
                department,
                "Principal Engineer" if department == "Engineering" and index % 17 == 0 else "Specialist",
                manager_id,
                team_id,
                join_date=joined,
                status=status,
            )

    skill_names = sorted({skill for _, _, _, _, skills in DEPARTMENT_DATA for skill in skills} |
                         {"Communication", "Leadership", "Excel", "Jira", "Cloud Security",
                          "Data Engineering", "Customer Success", "Service Design"})
    for skill in skill_names:
        skill_group = "Technical" if skill not in {
            "Communication", "Leadership", "Talent Acquisition", "Employee Relations",
            "People Analytics", "Financial Analysis", "Accounting", "Forecasting",
            "Marketing Analytics", "Content Strategy", "SEO", "Campaign Management",
            "Enterprise Sales", "Negotiation", "Account Management", "Project Management",
            "Process Improvement", "Business Analysis", "Product Strategy", "Roadmapping",
            "UX Research", "Customer Success", "Service Design", "Excel", "Jira",
        } else "Business"
        conn.execute("INSERT OR IGNORE INTO skills(name,skill_group) VALUES(?,?)", (skill, skill_group))
    skill_ids = {row["name"]: row["id"] for row in _rows(conn, "SELECT id,name FROM skills")}

    employees = _rows(
        conn, """SELECT id,department_id,team_id,employment_status
                 FROM employees WHERE company_id=? AND is_synthetic=1""", (company_id,)
    )
    department_name_by_id = {value: key for key, value in department_ids.items()}
    for employee in employees:
        department = department_name_by_id[employee["department_id"]]
        catalog = next(row[4] for row in DEPARTMENT_DATA if row[0] == department)
        selection = catalog[:]
        selection.extend(["Communication", "Leadership", "Excel", "Jira"])
        unique_skills = list(dict.fromkeys(selection))
        rng = random.Random(employee["id"] * 103)
        chosen = rng.sample(unique_skills, min(4 + employee["id"] % 3, len(unique_skills)))
        for index, skill in enumerate(chosen):
            conn.execute(
                "INSERT OR IGNORE INTO employee_skills(employee_id,skill_id,proficiency) VALUES(?,?,?)",
                (employee["id"], skill_ids[skill], 2 + ((employee["id"] + index) % 4)),
            )

    return {
        "team_ids": team_ids,
        "employee_index": employee_index,
        "department_head_ids": department_head_ids,
    }


def _seed_projects(conn, company_id, department_ids, team_ids, today):
    if conn.execute("SELECT COUNT(*) FROM projects WHERE company_id=? AND is_synthetic=1", (company_id,)).fetchone()[0]:
        return
    project_templates = {
        "Engineering": ["Enterprise API Modernisation", "Nexora Client Workspace", "Developer Platform Renewal", "Quality Automation", "Developer Portal"],
        "Data & Analytics": ["Nexora Insights Platform", "Trusted Data Foundation", "Customer Signal Analytics", "Governed Metrics", "Applied AI Studio"],
        "Product Management": ["Enterprise Experience Refresh", "Cloud Service Roadmap", "Product Discovery Sprint", "Design System", "Product Operations"],
        "Human Resources": ["People Experience Portal", "Talent Process Modernisation", "Workforce Insights", "Learning Marketplace", "Employee Listening"],
        "Finance": ["Financial Planning Workspace", "Spend Intelligence", "Controls Modernisation", "Commercial Forecasting", "Procurement Analytics"],
        "Marketing": ["Nexora Brand Studio", "Enterprise Demand Engine", "Cloud Launch Programme", "Customer Stories", "Marketing Measurement"],
        "Sales": ["Strategic Account Growth", "Cloud Partner Enablement", "Enterprise Pipeline Quality", "Account Planning", "Sales Intelligence"],
        "Cloud & Infrastructure": ["Cloud Landing Zone", "Platform Reliability Programme", "Infrastructure Automation", "Cloud FinOps", "Service Observability"],
        "Cybersecurity": ["Zero Trust Rollout", "Security Operations Upgrade", "Cloud Risk Programme", "Application Security", "Identity Governance"],
        "Business Operations": ["Delivery Excellence", "Client Onboarding Journey", "Operations Automation", "Service Quality", "Programme Management"],
    }
    departments = {row["id"]: row["name"] for row in _rows(conn, "SELECT id,name FROM departments")}
    team_names = {row["id"]: row["name"] for row in _rows(conn, "SELECT id,name FROM teams")}
    status_cycle = ["Active", "Active", "Active", "Planned", "Completed"]
    skills_by_department = {name: skills for name, _, _, _, skills in DEPARTMENT_DATA}
    project_index = 0
    for department, titles in project_templates.items():
        team_options = [row["id"] for row in _rows(
            conn, "SELECT id FROM teams WHERE department_id=? ORDER BY id", (department_ids[department],)
        )]
        for index, title in enumerate(titles):
            project_index += 1
            start = today - timedelta(days=30 + ((project_index * 47) % 740))
            status = status_cycle[(project_index - 1) % len(status_cycle)]
            target_end = today + timedelta(days=90 + index * 30) if status != "Completed" else today - timedelta(days=25)
            conn.execute(
                """INSERT INTO projects(company_id,department_id,team_id,name,client_name,description,
                   required_skills,status,priority,start_date,target_end_date,is_synthetic)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,1)""",
                (
                    company_id, department_ids[department], team_options[index % len(team_options)],
                    title, "Nexora Internal Programme",
                    f"Fictional Nexora {department.lower()} initiative supporting enterprise delivery.",
                    ", ".join(skills_by_department[department][:3]), status,
                    ["High", "Medium", "Low"][project_index % 3],
                    start.isoformat(), target_end.isoformat(),
                ),
            )
    project_ids = _rows(conn, "SELECT id,team_id FROM projects WHERE company_id=? AND is_synthetic=1", (company_id,))
    projects_by_team = {}
    for project in project_ids:
        projects_by_team.setdefault(project["team_id"], []).append(project["id"])
    employees = _rows(
        conn, "SELECT id,team_id,employment_status FROM employees WHERE company_id=? AND is_synthetic=1 AND team_id IS NOT NULL",
        (company_id,),
    )
    for employee in employees:
        if employee["employment_status"] == "Separated":
            continue
        choices = projects_by_team.get(employee["team_id"], [])
        if not choices:
            continue
        allocation = [55, 65, 75, 80, 90, 100][employee["id"] % 6]
        conn.execute(
            "INSERT OR IGNORE INTO project_allocations(employee_id,project_id,allocation_pct,allocated_at) VALUES(?,?,?,?)",
            (employee["id"], choices[employee["id"] % len(choices)], allocation, datetime.now().isoformat(timespec="seconds")),
        )


def _seed_jobs(conn, company_id, department_ids, location_ids, today):
    for title, department, description, required, experience, low, high, vacancies in DEMO_JOBS:
        legacy_department = "Analytics" if department == "Data & Analytics" else department
        existing = conn.execute(
            "SELECT id FROM jobs WHERE lower(title)=lower(?) AND lower(department) IN (lower(?),lower(?))",
            (title, department, legacy_department),
        ).fetchone()
        if existing:
            conn.execute(
                """UPDATE jobs SET department=?,department_id=?,location_id=?,salary_min_lpa=?,salary_max_lpa=?,
                   vacancies=?,is_synthetic=1 WHERE id=?""",
                (department, department_ids[department], location_ids["Bengaluru"], low, high, vacancies, existing["id"]),
            )
            continue
        conn.execute(
            """INSERT INTO jobs(title,department,description,required_skills,min_experience,status,created_at,
               department_id,location_id,salary_min_lpa,salary_max_lpa,vacancies,is_synthetic)
               VALUES(?,?,?,?,?,'Open',?,?,?,?,?,?,1)""",
            (
                title, department, description, required, experience,
                (today - timedelta(days=45)).isoformat() + "T09:00:00",
                department_ids[department], location_ids["Bengaluru"], low, high, vacancies,
            ),
        )

    department_name_map = {"Analytics": "Data & Analytics"}
    for row in DEPARTMENT_DATA:
        department_name_map[row[0]] = row[0]
    for old_name, department in department_name_map.items():
        conn.execute(
            """UPDATE jobs SET department=?,department_id=?,
               location_id=COALESCE(location_id,?) WHERE department=?""",
            (department, department_ids[department], location_ids["Bengaluru"], old_name),
        )
    conn.execute(
        """UPDATE jobs SET is_synthetic=1 WHERE title IN
           ('Data Analyst','Business Analyst','Python Developer','Marketing Analyst')
           AND department IN ('Analytics','Data & Analytics','Business Operations','Engineering','Marketing')"""
    )
def _seed_candidates_and_applications(conn, today):
    conn.execute(
        """UPDATE candidates SET is_synthetic=1
           WHERE email GLOB 'candidate[0-9]*@example.com'"""
    )
    conn.execute(
        """UPDATE applications SET is_synthetic=1
           WHERE candidate_id IN (SELECT id FROM candidates WHERE is_synthetic=1)"""
    )
    existing = conn.execute(
        "SELECT COUNT(*) FROM candidates WHERE email LIKE 'demo.%@nexora.example'"
    ).fetchone()[0]
    if existing:
        return
    jobs = _rows(
        conn, """SELECT id,title,department,required_skills,min_experience
                 FROM jobs WHERE status='Open' AND department_id IS NOT NULL ORDER BY id"""
    )
    if not jobs:
        return
    candidate_skills = {
        "Engineering": ["Python, SQL, API Design, Agile", "Java, SQL, Communication", "TypeScript, React, UX Research", "Python, Jira, API Design"],
        "Data & Analytics": ["SQL, Power BI, Statistics", "Python, SQL, Machine Learning", "SQL, Python, Data Engineering"],
        "Product Management": ["Product Strategy, Roadmapping, Agile", "UX Research, Jira, Communication"],
        "Human Resources": ["Talent Acquisition, People Analytics, Communication", "People Analytics, SQL, Power BI"],
        "Finance": ["Financial Analysis, Forecasting, Excel", "Accounting, Excel, Compliance"],
        "Marketing": ["Marketing Analytics, SEO, Campaign Management", "Content Strategy, Campaign Management"],
        "Sales": ["Enterprise Sales, CRM, Negotiation", "Account Management, CRM, Communication"],
        "Cloud & Infrastructure": ["AWS, Kubernetes, DevOps", "SRE, Linux, Kubernetes"],
        "Cybersecurity": ["Cybersecurity, SIEM, Incident Response", "Cloud Security, Compliance, Linux"],
        "Business Operations": ["Business Analysis, Process Improvement, Excel", "Project Management, Communication, Agile"],
    }
    created_candidates = []
    for index in range(72):
        job = jobs[index % len(jobs)]
        first = FIRST_NAMES[(index * 11 + 4) % len(FIRST_NAMES)]
        last = LAST_NAMES[(index * 9 + 3) % len(LAST_NAMES)]
        full_name = f"{first} {last}"
        email = f"demo.{index + 1:03d}@nexora.example"
        department = "Data & Analytics" if job["department"] == "Analytics" else job["department"]
        skills = candidate_skills.get(department, ["Python, SQL, Communication"])[index % len(candidate_skills.get(department, ["Python, SQL, Communication"]))]
        experience = float(1 + (index * 7) % 10)
        application_day = today - timedelta(days=(index * 17) % 550)
        cursor = conn.execute(
            """INSERT INTO candidates(full_name,email,phone,education,experience_years,skills,
               project_experience,certifications,created_at,is_synthetic)
               VALUES(?,?,?,?,?,?,?,?,?,1)""",
            (
                full_name, email, f"+91 90000 {index + 10000:05d}",
                ["B.Tech", "M.Tech", "B.Sc", "MBA", "B.E."][index % 5],
                experience, skills,
                f"Fictional delivery experience on {['cloud migration','analytics platform','enterprise workflow','security operations'][index % 4]} programmes.",
                "AWS Certified Cloud Practitioner" if "AWS" in skills else "",
                (application_day - timedelta(days=10)).isoformat() + "T09:00:00",
            ),
        )
        candidate_id = cursor.lastrowid
        created_candidates.append((candidate_id, job, application_day, skills, experience, index))

    for candidate_id, job, application_day, skills, experience, index in created_candidates:
        stage = ["Applied", "Screened", "Shortlisted", "Interview", "Selected", "Hired", "Rejected"][index % 7]
        cursor = conn.execute(
            """INSERT INTO applications(candidate_id,job_id,application_date,current_stage,
               match_score,notes,updated_at,is_synthetic)
               VALUES(?,?,?,?,?,?,?,1)""",
            (
                candidate_id, job["id"], application_day.isoformat(), stage,
                40 + ((index * 13) % 60), "Synthetic Nexora demonstration application.",
                (application_day + timedelta(days=5)).isoformat() + "T10:00:00",
            ),
        )
        application_id = cursor.lastrowid
        history_stages = {
            "Applied": ["Applied"],
            "Screened": ["Applied", "Screened"],
            "Shortlisted": ["Applied", "Screened", "Shortlisted"],
            "Interview": ["Applied", "Screened", "Shortlisted", "Interview"],
            "Selected": ["Applied", "Screened", "Shortlisted", "Interview", "Selected"],
            "Hired": ["Applied", "Screened", "Shortlisted", "Interview", "Selected", "Hired"],
            "Rejected": ["Applied", "Screened", "Rejected"],
        }[stage]
        for step, history_stage in enumerate(history_stages):
            event_date = application_day + timedelta(days=step * 4)
            conn.execute(
                "INSERT INTO stage_history(application_id,stage,changed_at,note) VALUES(?,?,?,?)",
                (
                    application_id, history_stage,
                    event_date.isoformat() + "T10:00:00",
                    "Synthetic Nexora demo event",
                ),
            )
        conn.execute(
            """INSERT INTO recruitment_costs(application_id,source,advertising_cost,recruiter_hours,hourly_rate,is_synthetic)
               VALUES(?,?,?,?,?,1)""",
            (application_id, ["Referral", "Careers site", "Professional network", "Campus"][index % 4],
             2200 + (index % 5) * 750, 1.5 + (index % 7) * .5, 1100),
        )
        if index % 3 == 0:
            interview_date = application_day + timedelta(days=10 + index % 18)
            conn.execute(
                """INSERT INTO interviews(application_id,scheduled_at,interview_type,status,notes,is_synthetic)
                   VALUES(?,?,?,?,?,1)""",
                (
                    application_id, interview_date.isoformat() + "T14:00:00",
                    ["Technical", "Hiring manager", "People & culture"][index % 3],
                    "Completed" if interview_date < today else "Scheduled",
                    "Synthetic interview record. No external invitation was sent.",
                ),
            )


def seed_company_demo_data(conn):
    now = datetime.now().isoformat(timespec="seconds")
    company = conn.execute("SELECT id FROM company WHERE name=?", (COMPANY["name"],)).fetchone()
    if company:
        company_id = company["id"]
    else:
        cursor = conn.execute(
            """INSERT INTO company(name,tagline,industry,business_model,headquarters,
               workforce_target,is_synthetic,created_at) VALUES(?,?,?,?,?,?,1,?)""",
            (
                COMPANY["name"], COMPANY["tagline"], COMPANY["industry"],
                COMPANY["business_model"], COMPANY["headquarters"],
                COMPANY["workforce_target"], now,
            ),
        )
        company_id = cursor.lastrowid

    location_ids = {}
    for name, state, office_type in LOCATION_DATA:
        conn.execute(
            "INSERT OR IGNORE INTO locations(company_id,name,state,office_type,is_synthetic) VALUES(?,?,?,?,1)",
            (company_id, name, state, office_type),
        )
        location_ids[name] = conn.execute(
            "SELECT id FROM locations WHERE company_id=? AND name=?", (company_id, name)
        ).fetchone()["id"]

    department_ids = {}
    for name, _, target, description, _ in DEPARTMENT_DATA:
        conn.execute(
            """INSERT OR IGNORE INTO departments(company_id,name,description,hiring_target,is_synthetic)
               VALUES(?,?,?,?,1)""",
            (company_id, name, description, target),
        )
        department_ids[name] = conn.execute(
            "SELECT id FROM departments WHERE company_id=? AND name=?", (company_id, name)
        ).fetchone()["id"]

    today = date.today()
    _seed_employee_directory(conn, company_id, department_ids, location_ids, today)
    team_ids = {
        (row["department"], row["name"]): row["id"]
        for row in _rows(
            conn, """SELECT t.id,t.name,d.name AS department FROM teams t
                     JOIN departments d ON d.id=t.department_id
                     WHERE d.company_id=? ORDER BY t.id""", (company_id,)
        )
    }
    _seed_projects(conn, company_id, department_ids, team_ids, today)
    _seed_jobs(conn, company_id, department_ids, location_ids, today)
    _seed_candidates_and_applications(conn, today)

    for title, provider, description, skill in LEARNING_RESOURCES:
        conn.execute(
            "INSERT OR IGNORE INTO learning_resources(title,provider,description,skill_name) VALUES(?,?,?,?)",
            (title, provider, description, skill),
        )
    for key, value in (
        ("email_enabled", "0"),
        ("smtp_host", ""),
        ("smtp_port", ""),
        ("notification_recipients", ""),
        ("require_human_approval", "1"),
    ):
        conn.execute(
            "INSERT OR IGNORE INTO notification_settings(setting_key,setting_value,updated_at) VALUES(?,?,?)",
            (key, value, now),
        )

    return {
        "company_id": company_id,
        "employees": conn.execute(
            "SELECT COUNT(*) FROM employees WHERE company_id=? AND is_synthetic=1", (company_id,)
        ).fetchone()[0],
        "departments": len(department_ids),
        "teams": conn.execute("SELECT COUNT(*) FROM teams WHERE is_synthetic=1").fetchone()[0],
        "projects": conn.execute("SELECT COUNT(*) FROM projects WHERE company_id=? AND is_synthetic=1", (company_id,)).fetchone()[0],
    }
