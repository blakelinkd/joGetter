# & 'C:\Program Files\Google\Chrome\Application\chrome.exe' --remote-debugging-port=9222
import datetime
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
        query_string = urllib.parse.quote("python OR javascript OR SQL")
        self.base_url = f'https://www.indeed.com/m/jobs?q={query_string}&l=remote&radius=600&limit=500&sort=date&fromage=1&from=mobRdr&vjk=10136f943542b7d7'
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
            # Checking if the job has already been visited
            visited_span = None  # Initialize visited_span to None for each job
            job_info = { 
                "company_name": "",
                "jobTitle": "",
                "link": "",
                "jobDescription": "",
                "easyApply": False
            }
            try:
                visited_span = WebDriverWait(job, 0.2).until(
                    EC.presence_of_element_located((By.XPATH, ".//span[contains(text(), 'Visited')]"))
                )
            except:
                pass
            if visited_span:
                pass
            
            try:
                easily_apply_span = WebDriverWait(job, 0.2).until(
                    EC.presence_of_element_located((By.XPATH, ".//span[contains(text(), 'Easily apply')]"))
                )
                self.easy_apply_count += 1
                job_info["easyApply"] = True
            except TimeoutException:
                pass

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
                    WebDriverWait(self.driver, 0.5).until(
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
                        print('Continuing...')
                
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
                    # self.driver.get("https://www.indeed.com")
                    # wait 5
                    # time.sleep(random.randint(3, 6))
                    self.driver.get(job_data["link"])
                    self.driver.implicitly_wait(3)     

                    try:
                            alert = Alert(self.driver)
                            alert.accept()
                            print(f"\033[93malert closed.\033[0m")
                    except:
                        pass

                    # try:
                    #     # Wait up to 30 seconds until the specific element is found
                    #     WebDriverWait(self.driver, 3).until(
                    #         EC.presence_of_element_located((By.ID, "challenge-running"))
                    #     )
                    #     print("Element found. Verifying you are human. This may take a few seconds.")
                    #     # Play beep sound
                    #     frequency = 2500  # Set Frequency To 2500 Hertz
                    #     duration = 1000  # Set Duration To 1000 ms == 1 second
                    #     winsound.Beep(frequency, duration)
                    #     # Element is found, pause the program for 20 seconds
                    #     return

                    # except Exception as e:
                    #     print("Continuing with the rest of the program...")

                    try:
                        job_description = WebDriverWait(self.driver, 0.2).until(
                            EC.presence_of_element_located((By.ID, "jobDescriptionText"))
                        )
                        job_data["jobDescription"] = job_description.text
                    except:
                        print("Page is broken... Skipping")
                        continue
                    try:
                        company_name = WebDriverWait(self.driver, 0.2).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '#viewJobSSRRoot > div > div.css-1quav7f.eu4oa1w0 > div > div > div.jobsearch-JobComponent.css-u4y1in.eu4oa1w0 > div.jobsearch-InfoHeaderContainer.jobsearch-DesktopStickyContainer.css-zt53js.eu4oa1w0 > div:nth-child(1) > div.css-2wyr5j.eu4oa1w0 > div > div > div > div.css-1h46us2.eu4oa1w0 > div > span > a'))
                        )
                        job_data["companyName"] = company_name.text
                        job_data["homepage"] = company_name.get_attribute('href')
                        print(f"\033[92m{company_name.text}\033[0m")
                    except:
                        pass
                    try:
                        post_title = WebDriverWait(self.driver, 0.2).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "jobsearch-JobInfoHeader-title"))
                        )
                        if not post_title.text:
                            job_data["postTitle"] = post_title.text
                        print(f"\033[95m{post_title.text}\033[0m")
                    except:
                        pass
                    try:
                        location = WebDriverWait(self.driver, 0.2).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="viewJobSSRRoot"]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]'))
                        )
                        job_data["location"] = location.text
                    except:
                        pass
                    
                    try:
                        salary = WebDriverWait(self.driver, 0.2).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="salaryInfoAndJobType"]/span[1]'))
                        )
                        job_data["salary"] = salary.text
                    except:
                        pass

                    try:
                        benefits = WebDriverWait(self.driver, 0.2).until(
                            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="benefits"]/div/div/span/ul/li'))
                        )
                        benefits_list = [benefit.text for benefit in benefits]
                        job_data["benefits"] = ', '.join(benefits_list)

                        benefits_list = [benefit.text for benefit in benefits]
                    except:
                        pass

                    jk = job_data["jk"]
                    job_title = job_data["postTitle"]
                    encoded_text = quote_plus(job_data["jobDescription"])
                    link = f"http://localhost:5000/generate-document?jk={jk}&job_title={job_title}&job_description={encoded_text}"
                    job_data["generateLink"] = link
                    cursor.execute('''
                    INSERT INTO jobs (companyName, homepage, postTitle, location, salary, compatibilityRating, link, skills, jobDescription, benefits, createdAt, jk, generateLink, easyApply)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
                    ''', (job_data['companyName'], job_data['homepage'], job_data['postTitle'], job_data['location'], job_data['salary'], job_data['compatibilityRating'], 
                        job_data['link'], job_data['skills'], job_data['jobDescription'], job_data['benefits'], job_data["createdAt"], job_data["jk"], job_data["generateLink"], job_data["easyApply"]))

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
    os.system('python compatibility.py')
    os.system('python skills_nlp.py')
    os.system('python insert_skills.py')


if __name__ == "__main__":
    main()






