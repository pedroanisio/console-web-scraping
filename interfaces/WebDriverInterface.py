from abc import ABC, abstractmethod
from selenium import webdriver

class WebDriverInterface(ABC):
    @abstractmethod
    def _initiate_driver(self):
        pass

    @abstractmethod
    def get_driver(self)->webdriver:
        pass

    @abstractmethod
    def quit_driver(self):
        pass
