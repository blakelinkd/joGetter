import datetime
import random
import re
import time
import urllib
from urllib.parse import quote_plus
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import os
from selenium.webdriver.common.alert import Alert
import sqlite3
import cv_locator
import pywinauto
import chromedriver_autoinstaller
from setup import setup
from dotenv import load_dotenv

def extract_uuid(url):
    pattern = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', re.IGNORECASE)
    match = pattern.search(url)
    if match:
        return match.group(0)
    else:
        return None

import sqlite3
from math import sqrt

def create_outliers_table():
    # Connect to the SQLite database
    conn = sqlite3.connect('job_data.db')
    cursor = conn.cursor()
    # Drop the table if it exists and recreate it with the latest data
    cursor.executescript("""
    DROP TABLE IF EXISTS RecentJobPostOutliers;
    CREATE TABLE RecentJobPostOutliers AS
    WITH JobCounts AS (
        SELECT companyName, COUNT(*) AS jobCount
        FROM jobs
        WHERE companyName <> ''
        GROUP BY companyName
    ),
    Stats AS (
        SELECT AVG(jobCount) AS average, 
               (SUM((jobCount - (SELECT AVG(jobCount) FROM JobCounts)) * (jobCount - (SELECT AVG(jobCount) FROM JobCounts))) / COUNT(*)) AS variance
        FROM JobCounts
    )
    SELECT jc.companyName, jc.jobCount,
           (jc.jobCount - s.average) / (sqrt(s.variance)) AS z_score
    FROM JobCounts jc, Stats s
    WHERE jc.jobCount > s.average + (2 * (sqrt(s.variance)))
    ORDER BY z_score DESC;
    """)

def check_company_in_outliers(company_name):
    conn = sqlite3.connect('job_data.db')
    cursor = conn.cursor()

    # Prepare the query to check if the company exists in the newly created table
    query = """
    SELECT EXISTS(
        SELECT 1 FROM RecentJobPostOutliers WHERE companyName = ?
    );
    """
    
    # Execute the query with the company name as a parameter to prevent SQL injection
    cursor.execute(query, (company_name,))
    
    # Fetch the result
    exists = cursor.fetchone()[0]
    
    # Close the connection
    conn.close()
    
    # Return True if the company exists, False otherwise
    return exists == 1



def configure_chrome_driver():
    chromedriver_autoinstaller.install()
    options = Options()
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15"
    options.add_argument(f'user-agent={user_agent}')
    return webdriver.Chrome(options=options)

class DiceBot:
    def __init__(self):
        print('got driver.')
        self.links = set()
        self.resume_path = os.getenv('RESUME_PATH')
        self.high_compat = 0
        self.low_compat = 0
        self.medium_compat = 0
        self.easy_apply_count = 0
        self.job_description = ""
        self.driver = configure_chrome_driver()
        self.total_jobs_count = 0
        self.jobs = []
        self.pages = 0
        self.max_pages = 1
    def run(self, search_query="python"):
        load_dotenv()
        username = os.getenv('DICE_EMAIL_ADDRESS')
        password = os.getenv('DICE_PASSWORD')
        self.driver.get("https://www.dice.com/dashboard/login")
        self.driver.implicitly_wait(10)
        time.sleep(3)
        try:
            email_field = WebDriverWait(self.driver, 8).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            print(email_field)
            email_field.send_keys(username)
        except:
            print("No login fields found.")
            return

        try:
            password_field = WebDriverWait(self.driver, 8).until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            print(password_field)
            password_field.send_keys(password)
        except:
            print("No login fields found.")
            return

        try:
            password_field = WebDriverWait(self.driver, 8).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="loginDataSubmit"]/div[3]/div/button'))
            )
            print(password_field)
            password_field.click()
            time.sleep(4)
        except:
            print("No login fields found.")
            return


        time.sleep(3)


        query_string = urllib.parse.quote(search_query)
        self.base_url = f'https://www.dice.com/jobs?q={query_string}&location=Remote,%20OR,%20Oklahoma&latitude=43.00594549999999&longitude=-123.8925908&countryCode=US&locationPrecision=City&radius=30&radiusUnit=mi&page=1&pageSize=500&filters.easyApply=true&language=en&eid=4677'
        print('getting base_url')
        self.driver.get(self.base_url)
        print('done')
        time.sleep(3)
        while True:
            self.extract_links()
            if not self.go_to_next_page():
                break
        self.process_links()
        os.system('python clean_and_rank.py')
        create_outliers_table()
        self.apply_links()
        self.driver.quit()

    def extract_links(self):
        print('extracting links...')
        try:
            job_list = WebDriverWait(self.driver, 8).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "card"))
            )
        except:
            print("No job list found.")
            return
        
        if not job_list:
            print("No job list found.")
            return
        for job in job_list:
            visited_span = None  # Initialize visited_span to None for each job
            job_info = {
                "id": "",
                "company_name": "",
                "jobTitle": "",
                "link": "",
                "jobDescription": "",
                "location": "",
                "easyApply": False
            }
            try:
                visited_span = WebDriverWait(job, 0.2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, ".//span[contains(text(), 'applied')]"))
                )
            except:
                pass
            
            if visited_span:
                print('Job already visited. Skipping...')
                continue
            
            try:
                easily_apply_span = WebDriverWait(job, 4).until( 
                    EC.presence_of_element_located((By.CLASS_NAME, "ng-star-inserted"))
                )
                if easily_apply_span:
                    self.easy_apply_count += 1
                    job_info["easyApply"] = True
            except TimeoutException:
                print('skipping, not easy!')
                continue

            try:
                title_elm = WebDriverWait(job, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "card-title-link"))
                )
                if not title_elm:
                    print("No matching job title <span> found within <a> elements.")
                    continue
                job_info["jobTitle"] = title_elm.text
                if not title_elm.get_attribute('id'):
                    print("No 'id' attribute found in the <a> element.")
                    continue
                if not title_elm.get_attribute('id'):
                    print("No 'id' attribute found in the <a> element.")
                    continue
                job_info["id"] = title_elm.get_attribute('id')
                print(f"\033[94m{title_elm.text}\033[0m")
            except TimeoutException:
                print("No matching job title <span> found within <a> elements.")

            try:
                title_elm = WebDriverWait(job, 0.4).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "search-result-location"))
                )
                if not title_elm.text:
                    print("No matching job title <span> found within <a> elements.")
                    continue
                
                job_info["location"] = title_elm.text
                print(f"\033[33m{title_elm.text}\033[0m")
            except TimeoutException:
                print("No matching job title <span> found within <a> elements.")
            
            try:
                company_elm = WebDriverWait(job, 0.4).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-cy="search-result-company-name"]'))
                )
                if not company_elm.text:
                    print("No matching job title <span> found within <a> elements.")
                    continue

                job_info["company_name"] = company_elm.text
                print(f"\033[33m{company_elm.text}\033[0m")
            except TimeoutException:
                print("No matching job title <span> found within <a> elements.")



            
            self.total_jobs_count += 1
            self.jobs.append(job_info)
        print(f"\033[91m{self.total_jobs_count} new jobs found.\033[0m")

    def go_to_next_page(self):
        try:
            next_page_button = WebDriverWait(self.driver, random.randint(3, 8)).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@class='page-link' and contains(text(), '»')]"))
            )
            next_page_button.click()
            self.pages += 1
            time.sleep(random.randint(2, 5))
            return True
        except:
            print("No next page button found.")
            return False
        
    
    def apply_links(self):
                conn = sqlite3.connect('job_data.db')
                cursor = conn.cursor()
                job_count = 0
                flow = {
                    'easy_apply': False,
                     'replace_button': False,
                    'apply_button': False,
                     'next_button': False,
                     'resume_upload_button': False,
                     'drop_target': False,
                     'drop_target_gray': False,
                     'resume_dropped': False,
                }
                # print job_count out of self.total_jobs_count
                print(f"\033[93mProcessing {job_count} out of {self.total_jobs_count} jobs...\033[0m")

                # for link in self.links:
                cursor.execute("""
                 SELECT id, link, generateLink, postTitle, companyName FROM jobs WHERE link LIKE '%dice.com%'
                AND hasApplied = '0'
                AND thirdParty = '1'
                AND easyApply = '1'
                ORDER BY id DESC;
                """)
                
                rows = cursor.fetchall()
                # print length of rows
                print(f"Rows: {len(rows)}")
                for row in rows:
                    alert_closed = False
                    id = row[0]
                    link = row[1]
                    generateLink = row[2]
                    postTitle = row[3]
                    companyName = row[4]
                    if check_company_in_outliers(companyName):
                        print(f"Company {companyName} is in the outliers. Skipping...")
                        continue
                    self.driver.get(link)
                    self.driver.implicitly_wait(4)
                    try:
                        alert = Alert(self.driver)
                        alert.accept()
                        print(f"\033[93malert closed.\033[0m")
                        alert_closed = True
                    except:
                        pass
                    if alert_closed:
                        self.driver.get(link)
                        self.driver.implicitly_wait(4)
                        time.sleep(2)
                    print(f"Processing link: {postTitle}")
                    easy_apply = cv_locator.find_and_click_image("easy_apply.png", timeout=3)
                    flow['easy_apply'] = easy_apply
                    time.sleep(2)
                    if not easy_apply:
                        cursor.execute('''
                                           UPDATE jobs
                                           set hasApplied = 1
                                           where id = ?
                                        ''', (id,))
                        conn.commit()
                        print('already visited, row updated.')
                        continue

                    
                    if flow['easy_apply']:
                        is_replace_button_located = cv_locator.find_and_click_image('replace_button.png', timeout=3)
                        flow['replace_button'] = is_replace_button_located

                    if flow['replace_button']:
                        is_drop_target_located = cv_locator.find_and_click_image('drop_target.png', timeout=3)
                        flow['drop_target'] = is_drop_target_located
                        if flow['drop_target']:
                            time.sleep(2)

                    if flow['drop_target']:
                        try:
                            app = pywinauto.Application().connect(title_re="Open")
                            
                            if app:
                                # If you're using a script to generate your resume, call it here.
                                # try:
                                #     response = requests.get(generateLink)
                                #     if response.status_code == 200:
                                #         print("Request successful")
                                # except Exception as e:
                                #     print(f"An error occurred: {e}")
                                    
                                time.sleep(3)
                                print('App found')
                                window = app.Dialog
                                window.set_focus()
                                filename_field = window.Edit1
                                file_path = os.path.abspath(self.resume_path)
                                filename_field.type_keys(file_path)
                                time.sleep(2)
                                filename_field.type_keys('{ENTER}')
                                time.sleep(2)

                                app.Dialog.Open.click()
                                time.sleep(5)

                        except Exception as e:
                            print(f"An error occurred: {e}")
                    
                    time.sleep(2)
                    
                    if flow['drop_target']:
                        is_resume_upload_button_located = cv_locator.find_and_click_image('resume_upload_button.png', timeout=3)
                        flow['resume_upload_button'] = is_resume_upload_button_located
                        if flow['resume_upload_button']:
                            time.sleep(2)

                    initial_url = self.driver.current_url

                    # find and click next_button.png
                    if flow['resume_upload_button']:
                        is_next_button_located = cv_locator.find_and_click_image('next_button.png', timeout=3)
                        flow['next_button'] = is_next_button_located

                    # Get the new URL
                    new_url = self.driver.current_url
                    # Compare the URLs to see if they are different
                    if flow['next_button']:
                        if new_url != initial_url:
                            print("The URL has changed after clicking the button.")
                            safe_forward = True
                        else:
                            continue
                    time.sleep(2)

                    if flow['next_button']:
                        is_apply_button_located = cv_locator.find_and_click_image('apply_button.png', timeout=3)
                        if is_apply_button_located:
                            print('Clicked apply_button.png')
                            cursor.execute('''
                                        UPDATE jobs
                                        SET hasApplied = 1
                                        WHERE id = ?
                                        ''', (id,))
                            conn.commit()




    def process_links(self):
            conn = sqlite3.connect('job_data.db')
            cursor = conn.cursor()
            job_count = 0
            print(f"\033[93mProcessing {job_count} out of {self.total_jobs_count} jobs...\033[0m")

            # for link in self.links:
            for job in self.jobs:
                jk_param = job["id"]

                try:
                    jk_param = job["id"]
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
                    print('jk: ', jk_param)
                    job_data = {
                        "companyName": job["company_name"],
                        "homepage": "",
                        "postTitle": job["jobTitle"],
                        "location": "",
                        "salary": "",
                        "compatibilityRating": "",
                        "link": job["link"],
                        "skills": "",
                        "jobDescription": "",
                        "benefits": "",
                        "createdAt": "",
                        "jk": jk_param,
                        "generateLink": "",
                        "easyApply": job["easyApply"],

                    }

                    job_data["createdAt"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    my_link = f"https://www.dice.com/job-detail/{job['id']}?searchlink=search%2F%3Fq%3DPython%26location%3DRemote%2C%2520OR%2C%2520USA%26latitude%3D43.00594549999999%26longitude%3D-123.8925908%26countryCode%3DUS%26locationPrecision%3DCity%26radius%3D30%26radiusUnit%3Dmi%26page%3D1%26pageSize%3D20%26language%3Den%26eid%3D4677&searchId=f97338a8-6920-46d5-8ac2-ca82871c04ef"
                    self.driver.get(my_link)
                    self.driver.implicitly_wait(3)
                    job_data["link"] = my_link

                    try:
                            alert = Alert(self.driver)
                            alert.accept()
                            print(f"\033[93malert closed.\033[0m")
                    except:
                        pass


                    try:
                        app_submitted = WebDriverWait(self.driver, 2).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "app-text"))
                        )
                        if app_submitted.text.contains("Application Submitted"):
                            print("applied already... Skipping")
                            continue
                    except:
                        pass
                        
                    

                    try:
                        job_description = WebDriverWait(self.driver, 0.2).until(
                            EC.presence_of_element_located((By.ID, "jobDescription"))
                        )
                        job_data["jobDescription"] = job_description.text
                    except:
                        print("Page is broken... Skipping")
                        continue
                    print(f"\033[92m{job_data['skills']}\033[0m")

                    
                    third_party = False
                    try:
                        job_description = WebDriverWait(self.driver, 0.2).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="widgetContainer"]/div[1]/div/h2'))
                        )
                        # print html contents of job_description
                        print(job_description.get_attribute('innerHTML'))
                        if job_description:
                            third_party = True
                            print("third party, not applying.")
                    except:
                        pass

                    job_data["companyName"] = job["company_name"]
                    job_data["jobTitle"] = job["jobTitle"]
                    job_data["location"] = job["location"]
                    job_data["salary"] = ""
                    jk = job["id"]
                    job_title = quote_plus(job_data["postTitle"])
                    encoded_text = quote_plus(job_data["jobDescription"])
                    link = f"http://localhost:5000/generate-document?jk={jk}&job_title={job_title}&job_description={encoded_text}"
                    job_data["generateLink"] = link
                    print(f'link: {job_data["generateLink"]}')
                    print(f"\033[96m{job_data['skills']}\033[0m")

                    if third_party == True:
                        third_party = 1
                    else:
                        third_party = 0
                    cursor.execute('''
                    INSERT INTO jobs (companyName, homepage, postTitle, location, salary, compatibilityRating, link, skills, jobDescription, benefits, createdAt, jk, generateLink, easyApply, thirdParty)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (job_data['companyName'], job_data['homepage'], job_data['postTitle'], job_data['location'], job_data['salary'], job_data['compatibilityRating'], 
                        job_data['link'], job_data['skills'], job_data['jobDescription'], job_data['benefits'], job_data["createdAt"], job_data["jk"], job_data["generateLink"], job_data["easyApply"], third_party))

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
    search_query=input("\033[91mSearch query: \033[0m")
    bot = DiceBot()
    bot.run(search_query)
    


if __name__ == "__main__":
    setup()
    main()






