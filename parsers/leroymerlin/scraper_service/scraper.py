import math
from dataclasses import dataclass

import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@dataclass
class Scraper:
    url: str
    driver: uc.Chrome

    def __post_init__(self):
        """
        Создание драйвера браузера и объекта Soup для дальнейшего парсинага.
        """
        self.driver.get(self.url)

        # Ожидание прогрузки страницы до определенного элемента
        # У страницы индекса и продукта они разные

        timeout = 5
        if "product" in self.url:
            element_present = EC.presence_of_element_located(
                (By.ID, "reviews")
            )
        else:
            element_present = EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//div[@role="navigation" and @aria-label="Pagination"]',
                )
            )
        WebDriverWait(self.driver, timeout).until(element_present)

        self.html = self.driver.page_source
        self.soup = BeautifulSoup(self.html, "lxml")

    @property
    def get_pagination_number(self):
        """
        Получение общего количества продуктов в данной категории
        """
        result = self.soup.find("div", class_="phfwh3v_plp").text
        number = int(result.split()[0]) / 30
        rounded_pages = math.ceil(number)
        return rounded_pages
