from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from interfaces.LoggerInterface import LoggerInterface

class Browser:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Browser, cls).__new__(cls)
        return cls._instance

    def __init__(self, engine=None, logger: LoggerInterface = None, session_manager=None):
        if not hasattr(self, 'initialized'):
            self.engine = engine
            self.driver = self.engine.get_driver()
            self.logger = logger
            self.hooks = {}
            self.session_manager = session_manager
            if self.session_manager:
                session_manager.set_driver(self.driver)
                self._set_hook("after_interaction", lambda url_provider: self.session_manager.validate(url_provider()))
            self.initialized = True

    def _set_hook(self,trigger, hook):
            self.hooks[trigger] = hook

    def _close_browser(self):
        try:
            self.engine.quit_driver()
            if self.logger:
                self.logger.log_info("Session destroyed successfully.")
        except Exception as e:
            if self.logger:
                self.logger.log_error(f"Error destroying session: {e}")
            raise            

    def perform_interaction(self, url, data=None, method='GET'):
        """
        Perform an interaction with the web page.

        Args:
            url (str): The URL to interact with.
            data (dict, optional): The data to send in a POST request.
            method (str): The HTTP method to use, either 'GET' or 'POST'.

        Returns:
            response: The response object from the interaction.
        """
        try:
            self.logger.log_info(f"Performing interaction with URL: {url}")
            self.driver.get(url)
            if method == 'POST' and data:
                self.driver.execute_script("fetch(arguments[0], {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(arguments[1])})", url, data)
            response = self.driver.page_source
            self.logger.log_info(f"Interaction with URL: {url} completed successfully.")
            self.hooks['after_interaction'](lambda: url)
            return response
        except Exception as e:
            self.logger.log_error(f"An error occurred during interaction with {url}: {e}")
            raise

    def close(self):
        try:
            self.logger.log_info(f"Shuting down browser.")            
            self._close_browser()
        except Exception as e:
            if self.logger:
                self.logger.log_error(f"Error closing and saving session: {e}")
            raise  