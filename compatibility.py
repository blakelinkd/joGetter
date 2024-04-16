import psycopg2

# Predefined dictionary of keywords with weights
keywords = {
    "Python": 3, "Perl": 1, "serverless": 1, "NoSQL": 1, "DB2": 1, "HTML": 1, "CSS": 1, "SASS": 1, "LESS": 1, "JavaScript": 2,
    "Java": 2, "Node.js": 2, "Agile": 1, "AWS": 1, "CloudFormation": 1, "Lambda": 2, "Jest": 1, "Cypress": 3,
    "SharePoint": 1, "DynamoDB": 1, "Django": 4, "Jira": 1, "Next.js": 4, "ORM": 1, "React": 4, "WCAG": 1, "SonarQube": 1,
    "Kubernetes": 2, "Prometheus": 1, "Grafana": 1, "Terraform": 1, "CI/CD": 2, "Docker": 2, "Flask": 3,
    "PostgreSQL": 1, "Nginx": 1, "Elasticsearch": 1, "Logstash": 1, "Kibana": 1, "BuildKite": 1, "Linux": 3,
    "Angular": 1, "Redux": 1, "SQLAlchemy": 1, "Prisma.js": 1, "FastAPI": 1, "ServiceNow": 1, "Pandas": 1, "Selenium": 3,
    "CSS": 1, "semantic HTML": 1, "TypeScript": 1, "SQL": 1, "support": 2, "C#": 1, ".NET": 1, "Blazor": 1,
    "Ubuntu": 2, "OOP": 1, "TDD": 1, "Responsive": 1, "SPA": 1, "Git": 2, "Jenkins": 2, "Redis": 1, "Spring": 1, "JPA": 1,
    "Microservice": 1, "API": 1, "ColdFusion": 2, "Lucee": 1, "CFML": 1, "REST": 1
}

# Modified function to calculate compatibility rating and get matched skills
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
