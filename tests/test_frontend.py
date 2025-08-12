import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://127.0.0.1:5000"

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # remover se quiser ver o navegador
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_cadastro_sucesso(driver):
    driver.get(f"{BASE_URL}/cadastro")
    wait = WebDriverWait(driver, 10)

    wait.until(EC.presence_of_element_located((By.ID, "formCadastro")))

    driver.find_element(By.ID, "nome").send_keys("Usuário Teste")
    driver.find_element(By.ID, "email").send_keys("teste@exemplo.com")
    driver.find_element(By.ID, "senha").send_keys("123456")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    mensagem = wait.until(lambda d: d.find_element(By.ID, "mensagem").text.strip() != "")
    text = driver.find_element(By.ID, "mensagem").text.lower()
    assert "sucesso" in text

def test_cadastro_usuario_existente(driver):
    driver.get(f"{BASE_URL}/cadastro")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "formCadastro")))

    driver.find_element(By.ID, "nome").clear()
    driver.find_element(By.ID, "nome").send_keys("Usuário Teste 2")
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "email").send_keys("teste@exemplo.com")  # email já cadastrado
    driver.find_element(By.ID, "senha").clear()
    driver.find_element(By.ID, "senha").send_keys("654321")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    mensagem = wait.until(lambda d: d.find_element(By.ID, "mensagem").text.strip() != "")
    text = driver.find_element(By.ID, "mensagem").text.lower()
    assert "já cadastrado" in text

def test_login_sucesso(driver):
    driver.get(f"{BASE_URL}/login")
    wait = WebDriverWait(driver, 10)

    wait.until(EC.presence_of_element_located((By.ID, "formLogin")))

    driver.find_element(By.ID, "emailLogin").send_keys("teste@exemplo.com")
    driver.find_element(By.ID, "senhaLogin").send_keys("123456")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    mensagem = wait.until(lambda d: d.find_element(By.ID, "mensagemLogin").text.strip() != "")
    text = driver.find_element(By.ID, "mensagemLogin").text.lower()
    assert "bem-sucedido" in text

def test_login_erro(driver):
    driver.get(f"{BASE_URL}/login")
    wait = WebDriverWait(driver, 10)

    wait.until(EC.presence_of_element_located((By.ID, "formLogin")))

    driver.find_element(By.ID, "emailLogin").send_keys("invalido@exemplo.com")
    driver.find_element(By.ID, "senhaLogin").send_keys("senhaerrada")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    mensagem = wait.until(lambda d: d.find_element(By.ID, "mensagemLogin").text.strip() != "")
    text = driver.find_element(By.ID, "mensagemLogin").text.lower()
    assert "inválidas" in text or "inválido" in text
