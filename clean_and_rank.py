import sqlite3
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
import gensim.downloader as api

# Initialize NLP tools
nltk.download('stopwords')
nltk.download('wordnet')
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Load pre-trained GloVe embeddings
glove_model = api.load("glove-wiki-gigaword-100")

def clean_text(text):
    if text is None:
        return []
    words = nltk.word_tokenize(text.lower())
    filtered_words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words and word.isalnum()]
    return filtered_words

def get_average_embedding(words, embedding_model):
    word_vectors = []

    for word in words:
        try:
            word_vectors.append(embedding_model[word])
        except KeyError:
            continue

    if not word_vectors:
        return np.zeros(embedding_model.vector_size)

    return np.mean(word_vectors, axis=0)

# Always load or define df from the database
conn = sqlite3.connect('job_data.db')
df = pd.read_sql_query("SELECT * FROM jobs", conn)

df['jobDescription'] = df['jobDescription'].apply(clean_text)

# Assume resume text is loaded into resume_text
with open('resume.md', 'r') as file:
    resume_text = file.read()

cleaned_resume_text = clean_text(resume_text)

resume_embedding = get_average_embedding(cleaned_resume_text, glove_model)

# Calculate compatibility scores using GloVe embeddings
df['compatibility_score'] = df['jobDescription'].apply(lambda x: cosine_similarity([get_average_embedding(x, glove_model)], [resume_embedding])[0][0])

# Update the database with new compatibility scores
cursor = conn.cursor()
for index, row in df.iterrows():
    cursor.execute("UPDATE jobs SET compatibility_score = ? WHERE id = ?", (row['compatibility_score'], row['id']))
conn.commit()
conn.close()

print("Compatibility scores have been updated in the existing database.")
