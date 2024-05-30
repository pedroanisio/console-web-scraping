# model/OreillySite.py

from interfaces.WebScrapeInterface import WebScrapeInterface
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from services.utils.FileLogger import FileLogger
from services.Browser import Browser
import time

class OreillySite(WebScrapeInterface):
    def __init__(self, browser: Browser, logger: FileLogger, config: dict):
        self.logger = logger
        self.is_authenticated = False
        self.browser = browser
        self.config = config
        self.logger.log_info("OreillySite model initialized.")
        self.driver = self.browser.driver

        # Warm up the URL
        logger.log_info("Warming up the URL.")
        self._warm_up_url()        
        
    def _warm_up_url(self):
        self.browser.perform_interaction(self.config['open_url'], method='GET')
        time.sleep(2)

    def authenticate(self, credentials):
        try:
            self.logger.log_info("Starting authentication process...")
            self.browser.perform_interaction(self.config['login_url'], method='GET')                                     

            # Save the current URL
            current_url = self.driver.current_url

            # Define a function to wait for URL change
            def wait_for_url_change(driver, old_url, timeout=10):
                wait = WebDriverWait(driver, timeout)
                wait.until(lambda driver: driver.current_url != old_url)
                return driver.current_url             

            # Fill in the email and submit
            self.logger.log_info("Filling in the email...")
            email_elem = self.driver.find_element(By.NAME, 'email')
            email_elem.send_keys(credentials['email'])
            email_elem.send_keys(Keys.RETURN)
            
            time.sleep(2)  # Wait for the AJAX request to complete
            
            # Fill in the password and submit
            self.logger.log_info("Filling in the password...")
            password_elem = self.driver.find_element(By.NAME, 'password')
            password_elem.send_keys(credentials['password'])
            password_elem.send_keys(Keys.RETURN)
            
            # Wait for the URL to change
            new_url = wait_for_url_change(self.driver, current_url)
            self.logger.log_info(f"Detected URL change to: {new_url}")
            self.browser.perform_interaction(new_url, method='GET')
            self.is_authenticated = True            
            self.logger.log_info("Authentication completed successfully.")
        except NoSuchElementException as e:
            self.logger.log_error(f"Element not found during authentication: {e}")
            raise
        except TimeoutException as e:
            self.logger.log_error(f"Timeout occurred during authentication: {e}")
            raise
        except Exception as e:
            self.logger.log_error(f"An error occurred during authentication: {e}")
            raise

    def check_authentication(self) -> bool:
        try:
            self.logger.log_info("Will check if session is authenticated")
            self.browser.perform_interaction(self.config['authed_url'], method='GET') 
            driver = self.browser.driver
            if self.config['authed_url'] in driver.current_url:
                self.logger.log_info("Found previous authentication.")
                self.is_authenticated = True
                return True
            else:
                self.logger.log_info(f"Unable to find previous authentication. Url is: {driver.current_url}")                
                self.is_authenticated = False
                return False
        except Exception as e:
            self.logger.log_error(f"An error occurred during authentication: {e}")
            raise
    
    def process_urls(self, urls: list) -> list:
        pass

    def _process_single_url(self, url: str) -> str:
        pass
