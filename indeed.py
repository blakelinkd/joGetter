# & 'C:\Program Files\Google\Chrome\Application\chrome.exe' --remote-debugging-port=9222
import datetime
import json
import random
import time
from urllib.parse import parse_qs, quote_plus, urlparse
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
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from selenium.webdriver.common.alert import Alert
import sqlite3
import winsound


def configure_chrome_driver():
    options = Options()
    options.debugger_address = "127.0.0.1:9222"
    # Specify the path to chromedriver if it's not in your PATH
    chrome_driver_path = './chromedriver-win64/chromedriver.exe'

    # Set the user-agent to mimic a Firefox browser on a Mac
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15"
    options.add_argument(f'user-agent={user_agent}')
    
    service = Service(executable_path=chrome_driver_path)
    return webdriver.Chrome(service=service, options=options)

class IndeedBot:
    def __init__(self):
        self.driver = configure_chrome_driver()
        self.links = set()
        self.high_compat = 0
        self.low_compat = 0
        self.medium_compat = 0
        self.easy_apply_count = 0
        self.job_description = ""
        query_string = urllib.parse.quote(input("type in your search query:"))
        days="7"
        self.base_url = f'https://www.indeed.com/m/jobs?q={query_string}&l=remote&radius=600&limit=500&sort=date&fromage={days}&from=mobRdr&vjk=10136f943542b7d7'
        self.total_jobs_count = 0
        self.jobs = []
        self.pages = 0
        self.max_pages = 1
    
    def detect_bot_detection(self):
        try:
            # Detect bot detection
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.ID, "challenge-running"))
            )
            print("Element found. Verifying you are human. This may take a few seconds.")
            frequency = 2500  # Set Frequency To 2500 Hertz
            duration = 1000  # Set Duration To 1000 ms == 1 second
            winsound.Beep(frequency, duration)
            time.sleep(20)
            return True
        except Exception as e:
            return False
    
    
    def run(self):
        self.driver.get(self.base_url)
        time.sleep(3)
        while True:
            if self.detect_bot_detection():
                break
            self.extract_links()
            if not self.go_to_next_page():
                break
        self.process_links()
        self.driver.quit()

    
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

    

    def process_links(self):
            conn = sqlite3.connect('job_data.db')
            cursor = conn.cursor()
            job_count = 0
            easy_app_count = 0
            # print job_count out of self.total_jobs_count
            print(f"\033[93mProcessing {job_count} out of {self.total_jobs_count} jobs...\033[0m")

            # for link in self.links:
            for job in self.jobs:
                try:
                    # Wait up to 30 seconds until the specific element is found
                    WebDriverWait(self.driver, 0.2).until(
                        EC.presence_of_element_located((By.ID, "challenge-running"))
                    )
                    print("Element found. Verifying you are human. This may take a few seconds.")
                    # Play beep sound
                    frequency = 2500  # Set Frequency To 2500 Hertz
                    duration = 1000  # Set Duration To 1000 ms == 1 second
                    winsound.Beep(frequency, duration)
                    return
                    # Element is found, pause the program for 20 seconds
                except Exception as e:
                        pass
                
                try:
                    parsed_url = urlparse(job["link"])
                    params = parse_qs(parsed_url.query)
                    jk_param = params.get('jk', [None])[0]
                    if not jk_param:
                        print("No 'jk' parameter found in URL")
                        continue

                    if jk_param:
                        # Query the database using the extracted 'jk' value
                        cursor.execute('''
                        SELECT * FROM jobs WHERE jk = ?
                        ''', (jk_param,))
                        row = cursor.fetchone()
                        if row:
                            print(f"Link {job} already exists in the database. Skipping...")
                            continue
                    job_data = {}
                    self.driver.get(job["link"])
                    self.driver.implicitly_wait(3)

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

                    job_data["jk"] = jk_param
                    job_data["jobDescription"] = data_dict.get("description", "").encode('utf-8').decode('unicode-escape')
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
                    cursor.execute('''
                        INSERT INTO jobs (companyName, logo, easyApply, postTitle, datePosted, validThrough, employmentType, applicantLocationRequirements, createdAt, link, jk, generateLink, jobDescription, locality, country, salaryMax, salaryMin)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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

                    job_count += 1
                    conn.commit()
                except TimeoutException:
                    print("TimeoutException")
                    continue
                except Exception as e:
                    print(f"An error occurred: {e}")
                    continue
            conn.close()
            print(f"\033[91m{job_count} jobs processed.\033[0m")
            print(f"\033[92m{self.easy_apply_count} easy apply jobs found.\033[0m")
            print(f"\033[93mDone.\033[0m")



def main():
    bot = IndeedBot()
    bot.run()
    # os.system('python compatibility.py')
    # os.system('python skills_nlp.py')
    # os.system('python insert_skills.py')


if __name__ == "__main__":
    main()






