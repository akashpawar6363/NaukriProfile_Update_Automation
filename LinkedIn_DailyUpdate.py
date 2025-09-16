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
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials from environment variables
LINKEDIN_EMAIL = os.getenv('NAUKRI_EMAIL')  # Using same email from Naukri
LINKEDIN_PASSWORD = os.getenv('NAUKRI_PASSWORD')  # Using same password from Naukri

# LinkedIn about section content
ABOUT_SECTION = """🚀 Full Stack & DevOps Engineer with 1.6+ years of experience turning complex business requirements into scalable, high-performance applications.

💡 **What I Bring:**
- 95% reduction in manual processes through intelligent automation
- 99.9% system reliability across enterprise applications
- Expertise in MERN Stack, Java Spring Boot, and AWS cloud solutions
- End-to-end ownership from requirement gathering to production deployment

🔧 **Current Focus:**
Leading SaaS development at Formonex Solutions, building laundry management platforms that serve multiple clients with tailored workflows and secure payment integration.

📈 **Key Achievements:**
- Engineered Financial Reconciliation System handling $1M+ transactions
- Built Patent Management System improving workflow efficiency by 40%
- Automated Indian Patent Office data extraction with 99% accuracy
- Reduced deployment time from hours to minutes using Docker & Jenkins

🎯 **Tech Stack:** Java, JavaScript, Python | React.js, Node.js, Spring Boot | AWS (EC2, S3, Lambda, RDS) | Docker, Jenkins, GitHub Actions

Always excited to discuss innovative solutions, cloud architecture, and automation opportunities!

#FullStackDeveloper #DevOps #AWS #MERN #SaaS #Automation"""

# Set up logging
logging.basicConfig(
    filename='linkedin_update.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class LinkedInProfileUpdater:
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
            # Navigate to LinkedIn login page
            self.driver.get('https://www.linkedin.com/login')
            logging.info("Navigated to LinkedIn login page")

            # Wait for and enter email
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_field.send_keys(email)

            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(password)

            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()

            # Wait for login to complete
            time.sleep(5)
            logging.info("Successfully logged in")
            return True

        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            return False

    def update_about_section(self, about_text):
        try:
            # Click on name to go to profile
            profile_name = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h3.profile-card-name.text-heading-large"))
            )
            profile_name.click()
            logging.info("Clicked on profile name")
            time.sleep(3)

            # Click on edit about section
            edit_buttons = self.driver.find_elements(By.CSS_SELECTOR, "use[href='#edit-medium']")
            for button in edit_buttons:
                # Find the parent button element
                edit_button = button.find_element(By.XPATH, "./ancestor::button")
                if edit_button.is_displayed():
                    edit_button.click()
                    logging.info("Clicked edit button")
                    break

            # Wait for the text area and clear it
            about_textarea = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.fb-gai-text__textarea"))
            )
            about_textarea.clear()
            about_textarea.send_keys(about_text)
            logging.info("Updated about section content")

            # Click Save button
            save_button = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-view-name='profile-form-save']"))
            )
            save_button.click()
            logging.info("Saved changes")

            # Wait for save to complete
            time.sleep(3)
            return True

        except Exception as e:
            logging.error(f"Failed to update about section: {str(e)}")
            return False

    def close_browser(self):
        self.driver.quit()
        logging.info("Browser closed")

def main():
    # Check if environment variables are set
    if not all([LINKEDIN_EMAIL, LINKEDIN_PASSWORD]):
        logging.error("Missing required environment variables. Please check your .env file")
        return

    updater = LinkedInProfileUpdater()
    
    try:
        if updater.login(LINKEDIN_EMAIL, LINKEDIN_PASSWORD):
            if updater.update_about_section(ABOUT_SECTION):
                logging.info("About section updated successfully")
            else:
                logging.error("Failed to update about section")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        updater.close_browser()

if __name__ == "__main__":
    main()