import os
import urllib.request 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import Chrome
import json
import google.generativeai as genai

class geradorPromptImagens:
    def __init__(self, config_file="./config/appsettings.json"):
        with open(config_file) as f:
            config = json.load(f)
        self.api_key = config["api_key"]
        genai.configure(api_key=self.api_key)
        self.model_name = "gemini-pro"

    def gerarPromptImagem(self, theme):
        # Construir o prompt com base no tema
        prompt = f'Finja que você é um usuário do Google Imagens e quer fazer uma pesquisa sobre: {theme}. Então digite apenas o prompt que geraria imagens mais precisas sobre isso (utilizando palavras chaves) com no máximo de 3 palavras'

        model = genai.GenerativeModel(self.model_name)
        response = model.generate_content(prompt)

        if response.text:
            return response.text
        else:
            print("A geração de conteúdo falhou. Verifique os logs para mais detalhes. Baixando imagens genéricas...")
            return theme 

def download_images_bing(search_query, qtd_images, nome_pasta, num_imagem):
    # Configurações do Chrome WebDriver undetected
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--start-maximized')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--log-level=3')
    options.add_argument('--disable-blink-features=AutomationControlled')

    # Inicializa o navegador
    driver = Chrome(options=options)
    driver.maximize_window()
    
    # URL do Google Imagens
    url = "https://www.bing.com/images/"
    driver.get(url)
    
    try:
        # Localiza o campo de pesquisa
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/header/form/div/input[1]'))
        )
        # Preenche o campo de pesquisa com a query
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        
        try:
            image_divs = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//img[contains(@alt, "Resultado de imagem")]')))
        except:
            print("Erro ao carregar as imagens. Tentando outro XPath...")
            pass

        images = image_divs
   
        # Caminho para a pasta 'img'
        base_dir = os.path.join(os.getcwd(), 'img')

        # Caminho para a pasta da query
        query_dir = os.path.join(base_dir, nome_pasta)

        # Cria o diretório para salvar as imagens se não existir
        if not os.path.exists(query_dir):
            os.makedirs(query_dir)
        
        downloaded_images = 0  # Variável para rastrear o número de imagens baixadas

        for img in images:
            if downloaded_images >= qtd_images:
                break  # Sai do loop se já tiver baixado o número desejado de imagens

            try:
                img_url = img.get_attribute('src')
                if img_url:  # Verifica se a URL da imagem não é nulo
                    img_name = f"linha_{num_imagem}_img_{downloaded_images}.jpg"
                    img_path = os.path.join(query_dir, img_name)
                    urllib.request.urlretrieve(img_url, img_path)
                    print(f"Imagem {downloaded_images + 1} baixada: {img_path}")
                    downloaded_images += 1  # Incrementa o número de imagens baixadas
                else:
                    print(f"Imagem ignorada devido a URL nula.")
            except Exception as e:
                print(f"Erro ao baixar a imagem: {e}")

        # Verifica se o número de imagens baixadas é menor que qtd_images
        if downloaded_images < qtd_images:
            print(f"Apenas {downloaded_images} imagens foram baixadas em vez de {qtd_images}. Não sei como.")
       
    finally:
        # Fecha o navegador
        driver.quit()