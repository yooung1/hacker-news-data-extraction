from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import pandas as pd
import time


class RobotNews:
    def __init__(self, base_url, path, csv_path):
        self.csv_path = csv_path
        self.base_url = base_url
        self.service = Service(executable_path=path)
        self.driver = webdriver.Chrome(service=self.service)
        self.my_dict = {}

    # Função criada para esperar elemento carregar
    def wait_for_object_to_appear(self, time, xpath_name):
        try:
            WebDriverWait(self.driver, time).until(
                expected_conditions.presence_of_element_located((By.XPATH, xpath_name))
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


if __name__ == "__main__":
    print("Initializing Application\n")
    path = r"C:\Users\Young1\Desktop\Selenium Course\Hacker News\Drivers\chromedriver-win64\chromedriver.exe"
    url = "https://news.ycombinator.com/"
    csv_path = r"C:\Users\Young1\Desktop\Selenium Course\Hacker News\Data\\"
    print("Instantiating Object")
    bot = RobotNews(base_url=url, path=path, csv_path=csv_path)
    try:
        print("Opening browser\n")
        bot.open_browser()
        print("Extracting Data from Hacker News\n")
        bot.extract_data_from_website()
        print("Creating CSV file with all the data collected\n")
        bot.create_csv_file()
    finally:
        print("Finishing process")
        bot.close_connection()
