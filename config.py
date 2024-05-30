# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    LOG_FILE = os.getenv('LOG_FILE', 'logs/logfile.log')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    REMOTE_URL = os.getenv('REMOTE_URL', 'http://<selenium-grid-docker>:4444/wd/hub')
    SESSIONS_DIR = os.getenv('SESSIONS_DIR', 'data/')
    
    # Parse BROWSER_OPTIONS from a single string into a list
    BROWSER_OPTIONS = os.getenv('BROWSER_OPTIONS', '').split(' ')

    # Site-specific configurations
    SITES = {
        "oreilly": {
            "open_url": os.getenv('OREILLY_OPEN_URL', 'https://www.example.com'),
            "login_url": os.getenv('OREILLY_LOGIN_URL', 'https://www.example.com/login'),            
            "authed_url": os.getenv('OREILLY_AUTHED_URL', 'https://www.example.com/secure'),
            "credentials": {
                "email": os.getenv('OREILLY_EMAIL', 'username@example.com'),
                "password": os.getenv('OREILLY_PASSWORD', 'password')
            }
        }
    }
