from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from datetime import datetime
import logging
import pyautogui
import threading
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials from environment variables
NAUKRI_EMAIL = os.getenv('NAUKRI_EMAIL')
NAUKRI_PASSWORD = os.getenv('NAUKRI_PASSWORD')
RESUME_PATH = os.getenv('RESUME_PATH')

# Set up logging
logging.basicConfig(
    filename='naukri_update.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class NaukriProfileUpdater:
    def __init__(self):
        self.setup_browser()
        
    def setup_browser(self):
        # Set up Chrome options
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # Uncomment to run in headless mode
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Initialize the Chrome WebDriver
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 20)

    def login(self, email, password):
        try:
            # Navigate to Naukri login page
            self.driver.get('https://www.naukri.com/nlogin/login')
            logging.info("Navigated to Naukri login page")

            # Wait for and enter email
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "usernameField"))
            )
            email_field.send_keys(email)

            # Enter password
            password_field = self.driver.find_element(By.ID, "passwordField")
            password_field.send_keys(password)

            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
            login_button.click()

            # Wait for login to complete
            time.sleep(5)
            logging.info("Successfully logged in")
            return True

        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            return False

    def close_file_dialog(self):
        """Function to close file dialog if it appears"""
        time.sleep(1)  # Wait for dialog to appear
        pyautogui.press('esc')
        logging.info("Attempted to close file dialog")

    def update_profile(self):
        try:
            # Navigate to profile
            self.driver.get('https://www.naukri.com/mnjuser/profile')
            logging.info("Navigated to profile page")

            # Wait for profile page to load
            time.sleep(5)

            # Get the absolute path of the resume from environment variable
            resume_path = os.path.abspath(RESUME_PATH)
            
            # Find the file input element
            file_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "attachCV"))
            )

            # Create a thread to handle the file dialog closure
            dialog_closer = threading.Thread(target=self.close_file_dialog)
            dialog_closer.start()

            # Send the file path
            file_input.send_keys(resume_path)
            logging.info(f"Attempting to upload resume from: {resume_path}")
            print(f"Uploading resume from: {resume_path}")

            # Wait for the dialog closer thread to complete
            dialog_closer.join()

            # Wait for the upload to process
            time.sleep(15)

            logging.info("Resume upload process completed")
            print("Resume upload process completed")
            return True

        except Exception as e:
            logging.error(f"Profile update failed: {str(e)}")
            return False

    def close_browser(self):
        self.driver.quit()
        logging.info("Browser closed")

def main():
    # Check if environment variables are set
    if not all([NAUKRI_EMAIL, NAUKRI_PASSWORD, RESUME_PATH]):
        logging.error("Missing required environment variables. Please check your .env file")
        return

    updater = NaukriProfileUpdater()
    
    try:
        if updater.login(NAUKRI_EMAIL, NAUKRI_PASSWORD):
            if updater.update_profile():
                logging.info("Daily profile update completed successfully")
            else:
                logging.error("Failed to update profile")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        updater.close_browser()

if __name__ == "__main__":
    main()
