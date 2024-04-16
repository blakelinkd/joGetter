# & '/usr/bin/google-chrome' --remote-debugging-port=9222
import datetime
import json
import random
import time
from urllib.parse import parse_qs, quote_plus, urlparse
import winsound
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import urllib
from selenium.webdriver.chrome.service import Service 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import os
from selenium.webdriver.common.alert import Alert
import psycopg2
from psycopg2 import pool
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from dotenv import load_dotenv



def configure_chrome_driver():
    
    options = Options()
    options.debugger_address = "127.0.0.1:9222"
    # Specify the path to chromedriver if it's not in your PATH
    chrome_driver_path = './chromedriver-win64/chromedriver.exe'

    # Set the user-agent to mimic a Firefox browser on a Mac
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15"
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    service = Service(service=ChromeService(ChromeDriverManager().install()))
    time.sleep(random.uniform(1, 3))

    return webdriver.Chrome(service=service, options=options)






class IndeedBot:
    def __init__(self):
        load_dotenv()
        self.driver = configure_chrome_driver()
        self.pg_password = os.getenv('PG_PASSWORD')
        self.pg_username = os.getenv('PG_USERNAME')
        self.pg_host = os.getenv('PG_HOST')
        self.connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10,
                                                                   dbname="lucee",
                                                                   user=self.pg_username,
                                                                   password=self.pg_password,
                                                                   host=self.pg_host)
        
        self.links = set()
        self.high_compat = 0
        self.low_compat = 0
        self.medium_compat = 0
        self.easy_apply_count = 0
        self.job_description = ""
        # query_string = urllib.parse.quote(input("type in your search query:"))
        query_string = urllib.parse.quote(f"SRE, SDET, Django, software engineer, SDET, Software Developer, Python, React, Angular, JavaScript, Kubernetes, Docker, Developer, Engineer, Programmer")
        # query_string = urllib.parse.quote(f"python, react, linux, docker, kubernetes")

        days="last"
        self.location = "remote"
        self.base_url = f'https://www.indeed.com/m/jobs?q={query_string}&l={self.location}&radius=30&limit=500&sort=date&fromage={days}&from=mobRdr&vjk=10136f943542b7d7'
        self.total_jobs_count = 0
        self.jobs = []
        self.pages = 0
        self.max_pages = 1

                # Define a list of user agents that would visit a website from a desktop browser
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/87.0",
            # Add more user agents as needed
        ]

        # Initialize a counter to keep track of the number of iterations
        self.iteration_counter = 0
    
    def detect_bot_detection(self):
        try:
            # Detect bot detection
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.ID, "challenge-running"))
            )
            print("Element found. Verifying you are human. This may take a few seconds.")
            frequency = 2500  # Set Frequency To 2500 Hertz
            duration = 1000  # Set Duration To 1000 ms == 1 second
            # winsound.Beep(frequency, duration)
            time.sleep(20)
            return True
        except Exception as e:
            return False
    
    
    def run(self):
         # List of popular websites
        popular_websites = ["https://www.bing.com", "https://www.indeed.com", "https://www.google.com", "https://www.facebook.com", "https://www.youtube.com"]
        wait_time = random.uniform(3, 15)

        # Visit three random websites from the list
        for _ in range(3):
            random_website = random.choice(popular_websites)
            self.driver.get(random_website)

            # Wait for a random duration between 3 to 5 seconds
            time.sleep(wait_time)

        # Finally, visit the base URL
        self.driver.get(self.base_url)
        time.sleep(wait_time)
        self.detect_bot_detection()
        time.sleep(3)
        while True:
            if self.detect_bot_detection():
                break
            self.extract_links()
            if not self.go_to_next_page():
                break
        
        self.filter_jobs()
        self.process_links()
        self.driver.quit()
        return self.total_jobs_count

    
    def extract_links(self):
        if self.detect_bot_detection():
            return
        
        try:
            job_list = WebDriverWait(self.driver, random.randint(3, 8)).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "result"))
            )
        except:
            print("No job list found.")
            return

        for job in job_list:
            job_info = { 
                "link": "",
            }

            try:
                    title_elm = WebDriverWait(job, 0.2).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "jcs-JobTitle"))
                    )
                    job_info["link"] = title_elm.get_attribute("href")
                    job_info["jobTitle"] = title_elm.text
                    print(f"\033[94m{title_elm.text}\033[0m")
            except TimeoutException:
                print("No title or link found.")
            
            self.total_jobs_count += 1
            self.jobs.append(job_info)
        print(f"\033[91m{self.total_jobs_count} new jobs found.\033[0m")

    def go_to_next_page(self):
        try:
            next_page_button = WebDriverWait(self.driver, random.randint(3, 8)).until(
                EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Next Page']"))
            )
        except:
            print("No next page button found.")
            return False
        time.sleep(random.randint(2, 5))
        self.pages += 1
        next_page_button.click()
        return True

    def filter_jobs(self):
        # Get a database connection from the connection pool
        conn = self.connection_pool.getconn()
        cursor = conn.cursor()

        # Extract 'jk' values from the job links and add them to the jobs
        valid_jobs = []
        jk_values = []  # This will store just the 'jk' values for the SQL query
        for job in self.jobs:
            parsed_url = urlparse(job["link"])
            params = parse_qs(parsed_url.query)
            if 'jk' in params:  # Ensure 'jk' parameter exists
                job['jk'] = params['jk'][0]  # Add 'jk' directly to the job dict
                valid_jobs.append(job)
                jk_values.append(params['jk'][0])  # Collect 'jk' values for querying

        # Query the database to find which 'jk' values already exist
        existing_jks = set()
        if jk_values:  # Proceed only if there are any 'jk' values to check
            placeholders = ','.join(['%s'] * len(jk_values))
            cursor.execute(f'''
                SELECT jk FROM jobs WHERE jk IN ({placeholders})
            ''', tuple(jk_values))
            rows = cursor.fetchall()
            existing_jks = {row[0] for row in rows}  # Use a set for faster lookup

        # Filter valid_jobs to exclude those whose 'jk' value exists in the database
        filtered_jobs = [job for job in valid_jobs if job['jk'] not in existing_jks]

        # Update the jobs and total_jobs_count to reflect the filtered list
        self.jobs = filtered_jobs
        self.total_jobs_count = len(filtered_jobs)

        # Return the database connection to the pool
        self.connection_pool.putconn(conn)


    def process_links(self):

            try:
                conn = self.connection_pool.getconn()
                cursor = conn.cursor()
                job_count = 1
                easy_app_count = 0
                # print job_count out of self.total_jobs_count
                print(f"\033[93mProcessing {job_count} out of {self.total_jobs_count} jobs...\033[0m")

                # for link in self.links:
                for job in self.jobs:
                    if self.detect_bot_detection():
                        print('bot detected')
                        return
                    try:
                        job_data = {}
                        self.driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {
                            "headers": {
                                "Referer": "https://www.indeed.com/"
                            }
                        })
                        self.driver.get(job["link"])
                        self.driver.implicitly_wait(3)

                        # sleep between 1 and 4 seconds
                        time.sleep(random.randint(1, 4))

                        try:
                                alert = Alert(self.driver)
                                alert.accept()
                                print(f"\033[93malert closed.\033[0m")
                        except:
                            pass
                        # Use WebDriverWait to wait for the <script> tag to be present
                        script_element = WebDriverWait(self.driver, 4).until(
                            EC.presence_of_element_located((By.XPATH, "//script[@type='application/ld+json']"))
                        )

                        # Extract the JSON string from the <script> tag
                        json_str = script_element.get_attribute('innerHTML')

                        # Parse the JSON string into a Python dictionary
                        data_dict = json.loads(json_str)

                        job_data["jk"] = job['jk']
                        job_data["jobDescription"] = data_dict.get("description", "")

                        
                        job_data["locality"] = data_dict.get("jobLocation", {}).get("address", {}).get("addressLocality", "")
                        job_data["country"] = data_dict.get("jobLocation", {}).get("address", {}).get("addressCountry", "")  # Fixed to addressCountry
                        job_data["logo"] = data_dict.get("hiringOrganization", {}).get("logo", "").encode('utf-8').decode('unicode-escape')
                        job_data["easyApply"] = data_dict.get("directApply", "")
                        job_data["companyName"] = data_dict.get("hiringOrganization", {}).get("name", "")
                        job_data["postTitle"] = data_dict.get("title", "")
                        job_data["datePosted"] = data_dict.get("datePosted", "")
                        job_data["validThrough"] = data_dict.get("validThrough", "")
                        job_data["employmentType"] = ''.join(data_dict.get("employmentType", []))
                        job_data["applicantLocationRequirements"] = data_dict.get("applicantLocationRequirements", {}).get("name", "")
                        job_data["createdAt"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        job_data["link"] = job.get("link", "")
                        job_data["generateLink"] = f"http://localhost:5000/generate-document?jk={job_data.get('jk', '')}&job_title={job_data.get('postTitle', '')}&job_description={job_data.get('jobDescription', '')}"
                        job_data["salaryMin"] = data_dict.get("baseSalary", {}).get("value", {}).get("minValue", "")
                        job_data["salaryMax"] = data_dict.get("baseSalary", {}).get("value", {}).get("maxValue", "")

                        print(job_data["postTitle"])
                        job_data["easyApply"] = 1 if job_data['easyApply'] else 0
                        # Assuming job_data is the dictionary containing the job data to insert
                        if job_data['salaryMax'] == "":
                            job_data['salaryMax'] = None  # Replace empty string with None

                        if job_data['salaryMin'] == "":
                            job_data['salaryMin'] = None  # Replace empty string with None

                        # Check and replace empty string with None for date columns
                        if job_data['datePosted'] == "":
                            job_data['datePosted'] = None  # Replace empty string with None

                        if job_data['validThrough'] == "":
                            job_data['validThrough'] = None  # Replace empty string with None

                        cursor.execute('''
                            INSERT INTO jobs (companyname, logo, easyapply, posttitle, dateposted, validthrough, employmenttype, applicantlocationrequirements, createdat, link, jk, generatelink, jobdescription, locality, country, salarymax, salarymin)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ''', (
                                job_data['companyName'],
                                job_data['logo'],
                                job_data['easyApply'],
                                job_data['postTitle'],
                                job_data['datePosted'],
                                job_data['validThrough'],
                                job_data['employmentType'],
                                job_data['applicantLocationRequirements'],
                                job_data["createdAt"],
                                job_data['link'],
                                job_data['jk'],
                                job_data['generateLink'],
                                job_data['jobDescription'],
                                job_data['locality'],
                                job_data['country'],
                                job_data['salaryMax'],
                                job_data['salaryMin']
                            ))


                        conn.commit()
                        #print in yello job/total_jobs_count
                        print(f"\033[93m{job_count}/{self.total_jobs_count}\033[0m")
                        job_count += 1
                    except TimeoutException:
                        print("TimeoutException")
                        continue
                    except Exception as e:
                        print(f"An error occurred: {e}")
                        continue
                print(f"\033[93mDone.\033[0m")
            except Exception as e:
                print(f"An error occurred: {e}")
                conn.rollback()
            finally:
                self.connection_pool.putconn(conn)

def main():
    bot = IndeedBot()
    jobs = bot.run()
    os.system('python compatibility.py')

    if jobs > 0:
        duration = 1000  # Duration in milliseconds
        freq = 1000  # Frequency in Hertz
        winsound.Beep(freq, duration)

while True:
    main()
    # sleep between 5 and 10 minutes
    ra = random.uniform(5, 10)
    time.sleep(ra * 60)  # Wait for 5 minutes

