import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="session")
def driver():
    options = Options()
    options.add_argument("--headless")  # opcional: roda sem abrir janela
    options.add_argument("--window-size=1920,1080")
    service = Service()  # se precisar, especifique o path do chromedriver aqui
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()
