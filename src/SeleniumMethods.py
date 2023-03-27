from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import webbrowser

PATH = r".\\Drivers"


def initialize_driver():  # Initialization for selenium drivers. No need to call if not using selenium
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager(path=PATH).install()))


