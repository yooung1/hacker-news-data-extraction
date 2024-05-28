from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

class RobotNews:
    def __init__(self, base_url, csv_path):
        self.csv_path = csv_path
        self.base_url = base_url
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)
        self.my_dict = {}

    # Função criada para esperar elemento carregar
    def wait_for_object_to_appear(self, timeout, xpath_name):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath_name))
            )
        except:
            return False
        return True

    # Acesso ao Site Hacker news    
    def open_browser(self):
        start_time = time.time()
        self.driver.get(self.base_url)
        self.driver.maximize_window()
        xpath_to_find = "//div[@class='RNNXgb']"
        if self.wait_for_object_to_appear(10, xpath_to_find):
            print("Data ready to be extracted")
        else:
            print(f"Error while trying to find element {xpath_to_find}")

        end_time = time.time()
        print(f"Time elapsed for opening browser: {end_time - start_time} seconds")

    # Extrair dados -- Titulo e Link
    def extract_data_from_website(self):
        start_time = time.time()
        xpath = "//span[@class='titleline']"
        xpath_children_title = "./a"
        xpath_children_link = "./a"
        titles = []
        links = []
        if self.wait_for_object_to_appear(30, xpath):
            containers = self.driver.find_elements(By.XPATH, xpath)
            for item in containers:
                title = item.find_element(By.XPATH, xpath_children_title).text
                link = item.find_element(By.XPATH, xpath_children_link).get_attribute("href")
                titles.append(title)
                links.append(link)
            self.my_dict = {"Titles": titles, "Links": links}

        end_time = time.time()
        print(f"Time elapsed for extracting data: {end_time - start_time} seconds")

    # Criar arquivo CSV com os dados extraidos
    def create_csv_file(self):
        start_time = time.time()
        pd.DataFrame(self.my_dict).to_csv(self.csv_path + r"\HACKER_NEWS_DATA.csv", index=False)

        end_time = time.time()
        print(f"Time elapsed for creating CSV file: {end_time - start_time} seconds")

    # Fechar navegação
    def close_connection(self):
        self.driver.quit()

    # Método run para executar todas as etapas
    def run(self):
        self.open_browser()
        self.extract_data_from_website()
        self.create_csv_file()

if __name__ == "__main__":
    print("Initializing Application")
    url = "https://news.ycombinator.com/"
    csv_path = r"C:\Users\Young1\Desktop\Selenium Course\Hacker News\Data"
    print("Instantiating Object")
    bot = RobotNews(base_url=url, csv_path=csv_path)
    try:
        print("Initiating process")
        bot.run()
    finally:
        print("Finishing process")
        bot.close_connection()
