import pandas as pd
import psycopg2
from transformers import pipeline
import torch

# Check if CUDA is available
print(torch.cuda.is_available())  # Should return True if CUDA is properly set up

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname='lucee', 
    user='lucee', 
    password='lucee', 
    host='localhost', 
)

# Initialize the NER pipeline with GPU if available
device = 0 if torch.cuda.is_available() else -1  # Use GPU if available, else CPU
nlp = pipeline("token-classification", model="algiraldohe/lm-ner-linkedin-skills-recognition", device=device)

def extract_skills(descriptions):
    ner_results = nlp(descriptions)
    batch_skills = []
    for result in ner_results:
        skills = []
        for entity in result:
            if entity['entity'].startswith('B-TECH') or entity['entity'].startswith('I-TECH'):
                skill = entity['word'].replace('##', '')
                if len(skill) > 2:
                    skills.append(skill.capitalize())
        batch_skills.append(', '.join(sorted(set(skills))))
    return batch_skills

def update_user_skills_in_batches(conn, batch_size=10):
    cursor = conn.cursor()
    df = pd.read_sql_query("SELECT * FROM resume_uploads WHERE skills IS NULL OR skills = ''", conn)
    
    num_batches = len(df) // batch_size + (0 if len(df) % batch_size == 0 else 1)
    
    for i in range(num_batches):
        start_index = i * batch_size
        end_index = start_index + batch_size
        batch = df.iloc[start_index:end_index]
        descriptions = batch['resume_text'].tolist()
        
        batch_skills = extract_skills(descriptions)
        
        for j, row in batch.iterrows():
            # Use parameterized queries for safety and efficiency
            cursor.execute("UPDATE resume_uploads SET skills = %s WHERE id = %s", (batch_skills[j - start_index], row['id']))
        
        conn.commit()
        print(f"Batch {i+1}/{num_batches} processed.")

    cursor.close()

# Run the update function
update_user_skills_in_batches(conn, batch_size=100)

def update_job_skills_in_batches(conn, batch_size=10):
    cursor = conn.cursor()
    df = pd.read_sql_query("SELECT * FROM jobs WHERE skills IS NULL OR skills = ''", conn)
    
    num_batches = len(df) // batch_size + (0 if len(df) % batch_size == 0 else 1)
    
    for i in range(num_batches):
        start_index = i * batch_size
        end_index = start_index + batch_size
        batch = df.iloc[start_index:end_index]
        descriptions = batch['jobdescription'].tolist()
        
        batch_skills = extract_skills(descriptions)
        
        for j, row in batch.iterrows():
            # Use parameterized queries for safety and efficiency
            cursor.execute("UPDATE jobs SET skills = %s WHERE id = %s", (batch_skills[j - start_index], row['id']))
        
        conn.commit()
        print(f"Batch {i+1}/{num_batches} processed.")

    cursor.close()

# Run the update function
update_job_skills_in_batches(conn, batch_size=100)




# Close the database connection
conn.close()
