from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials from environment variables
LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL')  # Using same email from Naukri
LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')  # Using same password from Naukri

# LinkedIn about section content
ABOUT_SECTION = """Full Stack & DevOps Engineer with 1.6+ years of experience turning complex business requirements into scalable, high-performance applications.

What I Bring:
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
            # Navigate directly to the edit URL
            self.driver.get('https://www.linkedin.com/in/akashpawar2000/add-edit/SUMMARY/?profileFormEntryPoint=PROFILE_SECTION')
            logging.info("Navigated directly to edit about section")
            time.sleep(3)  # Wait for page to load completely

            # Wait for the specific textarea using the exact selector
            textarea_selector = "textarea.fb-gai-text__textarea.artdeco-text-input--input.artdeco-text-input__textarea.artdeco-text-input__textarea--align-top"
            about_textarea = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, textarea_selector))
            )
            
            # First ensure the textarea is visible and interactable
            self.driver.execute_script("arguments[0].scrollIntoView(true);", about_textarea)
            time.sleep(1)
            
            # Clear the textarea using multiple approaches to ensure it works
            # 1. Clear using Selenium
            about_textarea.clear()
            
            # 2. Clear using JavaScript
            self.driver.execute_script("arguments[0].value = '';", about_textarea)
            
            # 3. Send backspace keys to ensure it's clear
            about_textarea.send_keys(Keys.CONTROL + "a")  # Select all
            about_textarea.send_keys(Keys.DELETE)  # Delete selection
            
            logging.info("Cleared the textarea")
            time.sleep(1)  # Wait a moment after clearing
            
            # Replace emoji and special characters with plain text
            sanitized_text = about_text.encode('ascii', 'ignore').decode('ascii')
            
            # Use multiple approaches to set the text
            # 1. Set using JavaScript
            self.driver.execute_script("arguments[0].value = arguments[1];", about_textarea, sanitized_text)
            
            # 2. Set using Selenium
            about_textarea.send_keys(sanitized_text)
            
            # Trigger all relevant events
            self.driver.execute_script("""
                var element = arguments[0];
                element.dispatchEvent(new Event('change'));
                element.dispatchEvent(new Event('input'));
                element.dispatchEvent(new Event('blur'));
            """, about_textarea)
            
            logging.info("Updated about section content")
            time.sleep(2)  # Wait for content to settle

            # Click Save button
            save_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-view-name='profile-form-save']"))
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