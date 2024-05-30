from abc import ABC, abstractmethod
from selenium.common.exceptions import WebDriverException

class WebScrapeInterface(ABC):
    def __init__(self, driver):
        self.driver = driver
        self.is_authenticated = False

    @abstractmethod
    def authenticate(self, credentials)-> bool:
        pass

    @abstractmethod
    def check_authentication(self)-> bool:
        pass
    
    @abstractmethod
    def process_urls(self, urls: list)-> list:
        pass

    @abstractmethod
    def _process_single_url(self, url: str)-> str:
        pass

    @abstractmethod
    def _warm_up_url(self):
        pass    


