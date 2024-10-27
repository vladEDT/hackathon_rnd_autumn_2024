import json
import re
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Catalog:
    """Класс подготовки ссылок продуктов выбранных категорий."""

    index_catalog: List[str] = field(default_factory=list)
    full_catalog: List[str] = field(default_factory=list)

    def index_catalog_builder(self, soup):
        """Выгрузка ссылок из списка товаров на index странице."""
        products = soup.findAll("div", class_="phytpj4_plp largeCard")
        for product in products:
            result = product.find("a").get("href")
            product_url = f"https://leroymerlin.ru{result}/"
            self.index_catalog.append(product_url)

    @property
    def get_catalog(self):
        return self.index_catalog


@dataclass
class JsonBuilder:
    """
    Класс обслуживания сбора и формирования пакета данных о продукте
    после отработки скрепера.
    """

    product_file: List[Dict] = field(default_factory=list)

    def collect_product_content(self, soup):
        """Сборщик словаря с данными продуктов."""
        product_title = self.content_palaceholder(
            soup.find("h1", itemprop="name")
        )

        domain = self.content_palaceholder(
            soup.find("div", class_="visually-hidden")
        )

        product_url = re.sub(
            r":\d+", "", soup.find("meta", property="og:url").get("content")
        )

        product_description = self.clear_html(
            self.content_palaceholder(soup.find("section", id="description"))
        )

        current_price = soup.find("span", slot="price")
        best_price = soup.find("span", class_="n1qeynqz_pdp")
        product_price = self.digits_parsing(
            self.price_selector(current_price, best_price)
        )

        page_title = self.content_palaceholder(soup.title)

        page_description = self.content_palaceholder(
            soup.find("meta", property="og:description").get("content")
        )

        specifications, weight, product_type = self.load_specifications(soup)

        images = self.load_images(soup)

        data = {
            "domain": domain.text,
            "product_url": product_url,
            "product_title": product_title.text,
            "product_description": product_description,
            "price": product_price,
            "page_title": page_title.text,
            "page_description": page_description,
            "shipping_dimensions": {"weight": weight},
            "specifications": specifications,
            "product_type": product_type,
            "images": images,
        }

        self.product_file.append(data)

    def content_palaceholder(self, content):
        """Плейсхолдер для случаев, если контент не найден."""
        data = content if content else "-"
        return data

    def clear_html(self, content):
        """Очистка HTML от сервисных параметров."""
        output = re.sub(
            (
                r"<section[^>]*>|</section[^>]*>|<section-layout>|"
                r'</section-layout>|<div[^>]*>|</div[^>]*>|class="[^"]*"'
            ),
            "",
            str(content),
        )
        output = output.replace(" >", ">")
        return output

    def digits_parsing(self, content):
        """Убираем из цифр nspb"""
        data = re.sub(r"\D", "", content.text)
        return data

    def price_selector(self, current_price, best_price):
        """На сайте может публиковаться одна из двух цен."""
        if best_price:
            return best_price
        return current_price

    def extract_json_content(self, soup, substring_after, substring_before):
        """Забираем секцию из JSON блока."""
        json_block = soup.find("script", id="init").text

        json_section = json_block.split(substring_after)[1]
        json_section = json_section.split(substring_before)[0]

        return json_section

    def load_specifications(self, soup):
        """Блок выгрузки спецификаций продукта."""
        substring_after = '{"characteristics":'
        substring_before = ',"manuals"'

        json_section = self.extract_json_content(
            soup, substring_after, substring_before
        )

        characteristics = json.loads(json_section)

        full_specs = {
            item["term"]: item["definition"]
            for item in characteristics
            if item["key"] not in ("22088", "logistic_grossWeight")
        }
        weight = next(
            (
                item["definition"]
                for item in characteristics
                if item["key"] == "logistic_grossWeight"
            ),
            "-",
        )
        product_type = next(
            (
                item["definition"]
                for item in characteristics
                if item["key"] == "22088"
            ),
            "-",
        )

        return full_specs, weight, product_type

    def load_images(self, soup):
        """Блок выгрузки картинок."""
        substring_after = '"images":'
        substring_before = ',"videos"'

        json_section = self.extract_json_content(
            soup, substring_after, substring_before
        )
        characteristics = json.loads(json_section)
        images = [item["url"] for item in characteristics]
        return images
