# Professional Profile Auto-Updater

This project automates the daily profile update process on both Naukri.com and LinkedIn. It uses Selenium WebDriver to:
1. Log in to your Naukri account and update your resume
2. Log in to your LinkedIn account and update your about section

## Features

### Naukri.com Automation
- Automated login to Naukri.com
- Automatic resume upload
- Daily profile update

### LinkedIn Automation
- Automated login to LinkedIn
- Update About section with professional description
- Maintain consistent professional presence

### Common Features
- Secure credential management using environment variables
- Automatic handling of system dialogs
- Detailed logging for both platforms
- Scheduled execution capability

## Prerequisites

- Python 3.x
- Chrome browser installed
- Your resume file (supported formats: doc, docx, rtf, pdf, up to 2 MB)

## Installation

1. Clone this repository or download the code

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   - Copy `.env.example` to a new file named `.env`
   - Update the `.env` file with your credentials:
     ```
     NAUKRI_EMAIL=your_email@example.com
     NAUKRI_PASSWORD=your_password
     RESUME_PATH=path/to/your/resume.pdf
     LINKEDIN_EMAIL=your_email@example.com
     LINKEDIN_PASSWORD=your_password
     ```

4. Place your resume in the project directory and update the RESUME_PATH in .env accordingly

## Usage

You can run each script individually:

### Naukri Profile Update
```bash
python Naukri_DailyUpdate.py
```

The script will:
1. Open Chrome browser
2. Log in to your Naukri account
3. Navigate to your profile
4. Upload your resume
5. Update your profile
6. Log the results

### LinkedIn Profile Update
```bash
python LinkedIn_DailyUpdate.py
```

The script will:
1. Open Chrome browser
2. Log in to your LinkedIn account
3. Navigate to your profile
4. Update your about section
5. Save changes
6. Log the results

### Running Both Updates
You can run both updates using the batch file:
```bash
run_naukri_update.bat
```

This will:
1. Update your Naukri profile
2. Update your LinkedIn profile
3. Log results for both operations

## Scheduling the Script

### Windows Task Scheduler Setup

1. Create a batch file (run_naukri_update.bat) with the following content:
   ```batch
   @echo off
   cd /d "F:\Python_Automation\DailyUpdate_LinkedIn"
   python Naukri_DailyUpdate.py
   ```
   Replace the path with your actual project directory path.

2. Open Task Scheduler:
   - Press `Win + R`
   - Type `taskschd.msc` and press Enter

3. Create a new task:
   - Click "Create Task" in the right panel
   - General tab:
     - Name: "Naukri Profile Update"
     - Select "Run whether user is logged in or not"
     - Check "Run with highest privileges"

4. Triggers tab:
   - Click "New"
   - Select "Daily"
   - Set start time (e.g., 10:00 AM)
   - Click OK

5. Actions tab:
   - Click "New"
   - Action: "Start a program"
   - Program/script: Browse to your run_naukri_update.bat file
   - Click OK

6. Conditions tab:
   - Uncheck "Start the task only if the computer is on AC power"
   - Check "Wake the computer to run this task"

7. Settings tab:
   - Check "Run task as soon as possible after a scheduled start is missed"
   - Check "If the task fails, restart every:" and set to 5 minutes
   - Set "Attempt to restart up to: 3 times"

8. Click OK to save the task

The script will now run automatically every day at your specified time. Make sure:
- Your computer is either running or can wake from sleep
- You're logged into Windows
- The .env file contains correct credentials

## Important Notes

- Make sure your resume file is in a supported format (doc, docx, rtf, pdf)
- Resume file size should not exceed 2 MB
- Keep your `.env` file secure and never commit it to version control
- The script uses PyAutoGUI to handle system dialogs, so avoid moving your mouse during execution

## Logging

The script creates a log file `naukri_update.log` that tracks all actions and any errors that occur during execution.

## Security

- Never share your `.env` file
- Always use `.env.example` for version control
- Keep your credentials secure

## Troubleshooting

If you encounter issues:
1. Check the log file for error messages
2. Ensure your credentials are correct in the `.env` file
3. Verify your resume file exists and is in a supported format
4. Make sure you have a stable internet connection
