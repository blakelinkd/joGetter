# DiceBot: Automated Job Application Bot

DiceBot is an automated tool designed to streamline the job application process on Dice.com. By leveraging this bot, users can automatically apply to job postings that match specified criteria, such as job title or technology stack, significantly reducing the time and effort required in job searching.

## Features

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
    pip install -r requirements.txt
    ```
2. Configuration
- Create a `.env` file in the root directory with your Dice.com username and password:
```bash
USERNAME=your_dice_username
PASSWORD=your_dice_password
```

3. Usage
run run.bat to activate the virtual environment and start the program


## Notes
This only works in windows because of the pyautogui code
