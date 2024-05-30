# File: services/sessions/FileSessionStrategy.py
import pickle
import os
from config import Config

class FileSessionStrategy:
    def __init__(self, session_file:str) -> None:
        """
        Initializes the FileSessionStrategy with the specified session file.

        Args:
            session_file (str): The path to the session file.
        """
        ## use os.path.join instead of f-string
        self.session_file = os.path.join(Config.SESSIONS_DIR, session_file)


    def exists(self) -> bool:
        """
        Checks if the session file exists.

        Returns:
            bool: True if the session file exists, False otherwise.
        """
        return os.path.exists(self.session_file)

    def save(self, session_data: dict) -> None:
        """
        Saves the session data to the session file using pickle.

        Args:
            session_data (dict): The session data to save.
        """
        with open(self.session_file, 'wb') as file:
            pickle.dump(session_data, file)

    def load(self) -> dict:
        """
        Loads the session data from the session file using pickle if the file exists.

        Returns:
            dict: The loaded session data.

        Raises:
            FileNotFoundError: If the session file does not exist.
        """
        if os.path.exists(self.session_file):
            with open(self.session_file, 'rb') as file:
                return pickle.load(file)
        else:
            raise FileNotFoundError(f"The session file {self.session_file} does not exist.")
