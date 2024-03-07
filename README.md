# joGetter: Automated Job Application Bot

joGetter is an automated tool designed to streamline the job application process on Dice.com. By leveraging this bot, users can automatically apply to job postings that match specified criteria, such as job title or technology stack, significantly reducing the time and effort required in job searching.

## Features
- **NEW!** I've built an interface with ColdFusion that allows you to view and sort jobs that have been scraped.
- **NEW!** JoGetter will keep track of companies that are mass posting jobs and will avoid applying to those.
- Automated login to Dice.com
- Customizable job search queries
- Automatic extraction of job links
- Application to jobs with "Easy Apply" option
- Resume upload functionality
- Tracking and management of applied jobs

## Installation

Before you begin, ensure you have Python installed on your system. This project also requires a Chrome WebDriver to be installed and properly configured.

1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/blakelinkd/joGetter.git
    cd joGetter
    pip install venv
    python -m venv .venv
    .\.venv\Scripts\activate
    pip install -r requirements.txt
    ```
2. Configuration
- Create a `.env` file in the root directory with your Dice.com username and password:
```bash
USERNAME=your_dice_username
PASSWORD=your_dice_password
RESUME_PATH="../path/to/resume.pdf"
```

3. Usage
To start, after you have configured the script run this command
```bash
python dice.py
```
4. ColdFusion UI
If you're interested in using the GUI you'll need to have docker and docker-compose installed. After running the bot and collecting some data, you can run these commands to browse your jobs:
```bash
cd lucee_view
docker-compose up --build -d
```
Now you can visit [http://Localhost:8888](http://localhost:8888)



## Notes
- This only works in windows because of the pyautogui code
- When you run the program, it's going to take control of the browser and you'll have to leave it be while it's running or you'll mess things up.
