# File: services/ChromeRemote.py
from interfaces.WebDriverInterface import WebDriverInterface
from interfaces.LoggerInterface import LoggerInterface
from selenium import webdriver
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException, WebDriverException
import requests

class ChromeRemote(WebDriverInterface):
    def __init__(self, remote_server_url="http://10.10.10.185:4444", logger: LoggerInterface = None, options=None):
        self.remote_server_url = remote_server_url
        self.driver = None
        self.logger = logger
        self.options = options
        self._initiate_driver()

    def _verify_remote_server(self):
        """
        Verify if the remote server is reachable.
        """
        try:
            response = requests.get(self.remote_server_url, timeout=5)
            response.raise_for_status()
            if self.logger:
                self.logger.log_debug(f"Remote server {self.remote_server_url} is reachable.")
        except requests.RequestException as e:
            if self.logger:
                self.logger.log_error(f"Cannot reach remote server {self.remote_server_url}: {e}")
            raise WebDriverException(f"Cannot reach remote server {self.remote_server_url}: {e}")

    def _initiate_driver(self):
        """
        Set up the Selenium WebDriver with the specified options for remote execution.
        """
        try:
            if self.logger:
                self.logger.log_info("Setting up the browser...")
                self.logger.log_debug(f"Remote server URL: {self.remote_server_url}")
                self.logger.log_debug(f"Options: {self.options}")

            # Verify the remote server before attempting to create the driver
            self._verify_remote_server()

            chrome_options = webdriver.ChromeOptions()
            if self.options:
                for option in self.options:
                    chrome_options.add_argument(option)
            chrome_options.page_load_strategy = 'eager'

            # Create remote connection
            self.connection = RemoteConnection(self.remote_server_url)

            if self.logger:
                self.logger.log_debug("Attempting to create remote WebDriver session.")

            # Set up the remote WebDriver with a timeout
            self.driver = webdriver.Remote(
                command_executor=self.connection,
                options=chrome_options,
                keep_alive=True  # Keep the connection alive to prevent timeouts
            )
            
            if self.logger:
                self.logger.log_info("Browser setup completed successfully.")
        except TimeoutException as e:
            if self.logger:
                self.logger.log_error(f"Timeout while setting up the browser: {e}")
            raise
        except NoSuchElementException as e:
            if self.logger:
                self.logger.log_error(f"Element not found during setup: {e}")
            raise
        except WebDriverException as e:
            if self.logger:
                self.logger.log_error(f"WebDriverException occurred while setting up the browser: {e}")
            raise
        except Exception as e:
            if self.logger:
                self.logger.log_error(f"An unexpected error occurred: {e}")
            raise

    def get_driver(self) -> webdriver:
        if self.logger:
            self.logger.log_debug("Returning WebDriver instance.")
        return self.driver

    def quit_driver(self):
        if self.driver:
            self.driver.quit()
            if self.logger:
                self.logger.log_info("Browser closed successfully.")
