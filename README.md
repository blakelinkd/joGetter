# joGetter: Automated Job Application Bot

joGetter is an automated tool designed to streamline the job application process on Dice.com. By leveraging this bot, users can automatically apply to job postings that match specified criteria, such as job title or technology stack, significantly reducing the time and effort required in job searching.

## Features
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
To get started you can run this command in your terminal, or double click the icon of `run.bat`
```bash
./run.bat
```


## Notes
- This only works in windows because of the pyautogui code
- When you run the program, it's going to take control of the browser and you'll have to leave it be while it's running or you'll mess things up.
