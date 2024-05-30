# services/session/SessionManager.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from interfaces.LoggerInterface import LoggerInterface
from services.session.FileSessionStrategy import FileSessionStrategy
from services.utils.URLBasedUUIDGenerator import URLBasedUUIDGenerator

class SessionNotFoundException(Exception):
    pass

class SessionManager:
    def __init__(self, strategy=None, logger: LoggerInterface = None):
        """
        Initializes the SessionManager with a given strategy and logger.

        Args:
            strategy: The strategy to use for session management.
            logger (LoggerInterface): The logger instance for logging.
        """
        self.driver = None
        self.logger = logger
        self.strategy = strategy
        self.history = []

    def set_driver(self, driver):
        self.driver = driver

    def validate(self, url: str) -> None:
        """
        Validates the given URL by checking its domain against the history.
        If the domain is not in history, restores the session with the domain and its UUID.

        Args:
            url (str): The URL to be validated.

        Raises:
            Exception: If there is an issue with extracting the domain or getting the UUID.
        """
        try:
            self.logger.log_info(f"Check if request has previous session: {url}.")
            domain = URLBasedUUIDGenerator().extract_domain(url)
            uuid = URLBasedUUIDGenerator().get_uuid(url)
            self.strategy = FileSessionStrategy(uuid)
            # Check if domain is in history
            if domain in self.history:
                self.logger.log_info(f"Previous session data for {domain} was already restored.")
                self.logger.log_info(f"Starting session update for: {domain}")
                self._save_session(domain, uuid)
                return
            else:
                if self.strategy.exists():
                    self.logger.log_info(f"Previous session data for: {domain} was not restored yet. Restoring now.")
                    self._restore_session(domain)
                else:
                    self.logger.log_info(f"Saving session for: {domain} for the first time.")
                    self._save_session(domain, uuid)
                self.history.append(domain)
        except Exception as e:
            if self.logger:
                self.logger.log_error(f"Error validating URL: {e}")
            raise

    def _save_session(self, domain: str, uuid: str) -> None:
        """
        Saves the current session's cookies, local storage, and session storage incrementally.

        Args:
            domain (str): The domain of the session.
            uuid (str): The UUID of the session.

        Raises:
            Exception: If there is an issue with saving the session.
        """
        try:
            if self.logger:
                self.logger.log_info(f"Attempting to save session for domain: {domain} with UUID: {uuid}")
            # Retrieve existing session data if any
            try:
                existing_session_data = self.strategy.load()
                self.logger.log_info(f"Existing session data retrieved: {existing_session_data}")
            except FileNotFoundError:
                existing_session_data = None
                if self.logger:
                    self.logger.log_info("No existing session data found, creating new session data.")

            # Get current session data
            current_session_data = {
                'cookies': self.driver.get_cookies(),
                'local_storage': self.driver.execute_script("return window.localStorage;"),
                'session_storage': self.driver.execute_script("return window.sessionStorage;")
            }
            if self.logger:
                self.logger.log_debug(f"Current session data: {current_session_data}")

            # Merge and save session data
            self._merge_session(existing_session_data, current_session_data)

            if self.logger:
                self.logger.log_info("Session saved successfully.")
        except Exception as e:
            if self.logger:
                self.logger.log_error(f"Error saving session: {e}")
            raise
        
    def _merge_session(self, existing_session_data: dict, current_session_data: dict) -> None:
        """
        Merges the existing session data with the current session data and saves it.

        Args:
            existing_session_data (dict): The existing session data.
            current_session_data (dict): The current session data to merge.

        Raises:
            Exception: If there is an issue with saving the merged session.
        """
        try:
            if existing_session_data:
                for key, value in current_session_data.items():
                    if key in existing_session_data:
                        if isinstance(existing_session_data[key], list):
                            # Handle merging lists (e.g., cookies) by overwriting duplicates
                            existing_session_data[key] = self._merge_lists(existing_session_data[key], value)
                        elif isinstance(existing_session_data[key], dict):
                            # Handle merging dictionaries (e.g., localStorage, sessionStorage)
                            existing_session_data[key].update(value)
                    else:
                        existing_session_data[key] = value
                self.strategy.save(existing_session_data)
                if self.logger:
                    self.logger.log_info(f"Merged existing session data: {existing_session_data}")
            else:
                self.strategy.save(current_session_data)
                if self.logger:
                    self.logger.log_info(f"Saved new session data: {current_session_data}")
        except Exception as e:
            if self.logger:
                self.logger.log_error(f"Error merging session data: {e}")
            raise

    def _merge_lists(self, existing_list: list, current_list: list) -> list:
        """
        Merges two lists of dictionaries, overwriting duplicates based on a key (e.g., 'name' for cookies).

        Args:
            existing_list (list): The existing list of dictionaries.
            current_list (list): The current list of dictionaries.

        Returns:
            list: The merged list of dictionaries with duplicates overwritten.
        """
        key_name = 'name'  # Specify the key to determine duplicates, e.g., 'name' for cookies
        merged_dict = {item[key_name]: item for item in existing_list}
        for item in current_list:
            merged_dict[item[key_name]] = item
        return list(merged_dict.values())

    def _restore_session(self, domain: str) -> None:
        """
        Restores the session for the given domain.

        Args:
            domain (str): The domain of the session to restore.

        Raises:
            SessionNotFoundException: If the session file is not found.
            Exception: If there is an issue with restoring the session.
        """
        try:
            session_data = self.strategy.load()
            filtered_cookies = [cookie for cookie in session_data['cookies'] if domain in cookie['domain']]
            for cookie in filtered_cookies:
                try:
                    self.driver.add_cookie(cookie)
                except Exception as e:
                    if self.logger:
                        self.logger.log_error(f"Error adding cookie: {e}")
            for key, value in session_data['local_storage'].items():
                self.driver.execute_script(f"window.localStorage.setItem('{key}', '{value}');")
            for key, value in session_data['session_storage'].items():
                self.driver.execute_script(f"window.sessionStorage.setItem('{key}', '{value}');")
            self.driver.refresh()
            if self.logger:
                self.logger.log_info("Session restored successfully.")
        except FileNotFoundError:
            if self.logger:
                self.logger.log_error("Session file not found.")
            raise SessionNotFoundException("Session file not found.")
        except Exception as e:
            if self.logger:
                self.logger.log_error(f"Error restoring session: {e}")
            raise
