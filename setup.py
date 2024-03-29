import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def setup():
    database = "job_data.db"

    sql_create_jobs_table = """
    CREATE TABLE jobs (
	id INTEGER,
	postTitle TEXT,
	location TEXT,
	salary TEXT,
	compatibilityRating TEXT,
	hasApplied INTEGER DEFAULT (0),
	link TEXT,
	generateLink TEXT,
	skills TEXT,
	jobDescription TEXT,
	benefits TEXT,
	Resume BLOB,
	createdAt TEXT,
	companyName TEXT,
	jk TEXT,
	homepage TEXT,
	"source" TEXT,
	emails TEXT,
	websiteUrl TEXT,
	HREmail TEXT,
	PhoneNumber TEXT,
	hasBeenSearched INTEGER,
	experience INTEGER,
	HRName TEXT,
	emailSent INTEGER,
	easyApply INTEGER,
	interviewing INTEGER,
	compatibility_score INTEGER,
	missingSkills TEXT,
	thirdParty INTEGER,
	recruiterName TEXT,
	locality TEXT,
	country TEXT,
	logo TEXT,
	datePosted TEXT,
	validThrough TEXT,
	employmentType TEXT,
	jobLocationType TEXT,
	applicantLocationRequirements TEXT, salaryMax REAL, salaryMin REAL,
	CONSTRAINT JOBS_PK PRIMARY KEY (id)
    );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        create_table(conn, sql_create_jobs_table)
        conn.commit()
        conn.close()
    else:
        print("Error! cannot create the database connection.")

if __name__ == "__main__":
    setup()