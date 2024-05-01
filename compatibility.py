import psycopg2

# Predefined dictionary of keywords with weights
keywords = {
    "htmx": 5, "Ember.js": 5, "Backbone.js": 5, "Next.js": 5, "vue": 5, "svelte": 5, "typescript": 5, "devops": 2, "SDLC": 5, "Python": 9, "Perl": 3, "serverless": 2, "NoSQL": 1, "DB2": 1, "HTML": 1, "CSS": 3, "SASS": 2, "LESS": 2, "JavaScript": 5,
    "Java": 3, "ColdFusion": 4, "Node.js": 3, "Nodejs": 3, "Agile": 1, "AWS": 1, "CloudFormation": 1, "Lambda": 2, "pytest": 5, "nosetest":5, "playwright": 5, "Jest": 5, "Cypress": 5,
    "Moq":1, "mock": 2, "mocha": 2, "SharePoint": 1, "DynamoDB": 1, "Django": 4, "Jira": 1, "Next.js": 5, "Nextjs": 5, "ORM": 1, "React": 5, "WCAG": 3, "SonarQube": 1,
    "Kubernetes": 4, "Prometheus": 2, "Grafana": 3, "BDD": 5, "cucumber": 5, "gherkin": 5, "Terraform": 1, "CI/CD": 3, "Docker": 4, "integration": 3, "Flask": 5,
    "PostgreSQL": 2, "Nginx": 1, "Elasticsearch": 3, "Logstash": 2, "Kibana": 2, "BuildKite": 1, "Linux": 5,
    "Angular": 5, "Redux": 2, "SQLAlchemy": 1, "Prisma.js": 2, "FastAPI": 4, "ServiceNow": 1, "Pandas": 1, "Selenium": 5,
    "CSS": 1, "semantic HTML": 1, "TypeScript": 1, "SQL": 1, "support": 3, "C#": 3, ".NET": 3, "Blazor": 4,
    "Ubuntu": 2, "TDD": 5, "Responsive": 1, "SPA": 1, "Git": 4, "Jenkins": 4, "Redis": 1, "Spring": 1, "JPA": 1,
    "Microservice": 1, "API": 1, "ColdFusion": 2, "Lucee": 1, "CFML": 1, "REST": 1, "automation": 2, "testing": 2, 
}


def get_compatibility_rating_and_skills(description, keywords):
    skill_count = {}
    description_lower = description.lower()
    for keyword in keywords:
        if keyword.lower() in description_lower:
            skill_count[keyword] = keywords[keyword]
    compatibility_rating = sum(skill_count.values())
    sorted_skills = sorted(skill_count, key=lambda x: skill_count[x], reverse=True)
    return compatibility_rating, ', '.join(sorted_skills)

# Connect to the PostgreSQL database
try:
    conn = psycopg2.connect(
        dbname="lucee",
        user="lucee",
        password="lucee",
        host="localhost"
    )
except Exception as e:
    print(f"An error occurred: {e}")
    exit()
c = conn.cursor()

# Fetch all jobs from the database
c.execute("SELECT id, jobdescription FROM jobs")
jobs = c.fetchall()

# Calculate, update compatibilityRating, and skills for each job
for job in jobs:
    jobId, jobdescription = job
    compatibility_rating, matched_skills = get_compatibility_rating_and_skills(jobdescription, keywords)
    # Use %s as placeholder for PostgreSQL
    c.execute("UPDATE jobs SET compatibilityrating = %s, skills = %s WHERE id = %s", (compatibility_rating, matched_skills, jobId))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Compatibility ratings and matched skills updated successfully.")

# import psycopg2

# # Predefined list of keywords
# keywords = [
#     "Python", "Perl", "serverless", "NoSQL", "DB2", "HTML", "CSS", "SASS", "LESS", "JavaScript", "Java", "Node.js", "Agile", "AWS", "CloudFormation", "Lambda", "Jest", "Cypress",
#     "SharePoint", "DynamoDB", "Django", "Jira", "Next.js", "ORM", "React", "WCAG", "SonarQube", "Kubernetes", "Prometheus", "Grafana",
#     "Terraform", "CI/CD pipeline", "Docker", "Flask", "PostgreSQL", "Nginx", "Elasticsearch", "Logstash", "Kibana",
#     "BuildKite", "Linux", "LISP", "Angular", "Redux", "SQLAlchemy", "Prisma.js", "FastAPI", "ServiceNow", "Pandas", "Selenium", 
#     "CSS", "semantic HTML", "TypeScript", "SQL", "technical", "support", "C#", ".NET", "Blazor", "Ubuntu", "OOP", "TDD", "Responsive", "SPA"
#     "Git", "Jenkins", "Redis", "Spring", "JPA", "Microservice", "API", "ColdFusion", "Lucee", "CFML", "REST",
# ]

# # Modified function to calculate compatibility rating and get matched skills
# def get_compatibility_rating_and_skills(description, keywords):
#     skill_count = {}
#     description_lower = description.lower()
#     for keyword in keywords:
#         if keyword.lower() in description_lower:
#             skill_count[keyword] = 1
#     compatibility_rating = sum(skill_count.values())
#     sorted_skills = sorted(skill_count, key=lambda x: x)
#     return compatibility_rating, ', '.join(sorted_skills)

# # Connect to the PostgreSQL database
# try:
#     conn = psycopg2.connect(
#         dbname="lucee",
#         user="lucee",
#         password="lucee",
#         host="localhost"
#     )
# except Exception as e:
#     print(f"An error occurred: {e}")
#     exit()
# c = conn.cursor()

# # Fetch all jobs from the database
# c.execute("SELECT id, jobdescription FROM jobs")
# jobs = c.fetchall()

# # Calculate, update compatibilityRating, and skills for each job
# for job in jobs:
#     jobId, jobdescription = job
#     compatibility_rating, matched_skills = get_compatibility_rating_and_skills(jobdescription, keywords)
#     # Use %s as placeholder for PostgreSQL
#     c.execute("UPDATE jobs SET compatibilityrating = %s, skills = %s WHERE id = %s", (compatibility_rating, matched_skills, jobId))

# # Commit the changes and close the connection
# conn.commit()
# conn.close()

# print("Compatibility ratings and matched skills updated successfully.")
