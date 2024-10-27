import json
import time

import undetected_chromedriver as uc

from scraper_service.catalog_builder import Catalog, JsonBuilder
from scraper_service.scraper import Scraper


def initial_object_collection(source_url, driver):
    """
    Сбор данных о количестве страниц и сохранение объекта первой страницы в
    пулл последующего скреппинга.
    """
    start_page = Scraper(source_url, driver)
    total_pages = start_page.get_pagination_number
    index_catalog = [start_page]

    return total_pages, index_catalog


def urls_pull_object_collection(
    total_pages, delay_time, source_url, index_catalog, scraper_class, driver
):
    """Создаём массив из объектов с данными индекса страниц."""
    pattern = "{}?page={}"

    for pagination in range(2, total_pages + 1):
        time.sleep(delay_time)
        url = pattern.format(str(source_url), str(pagination))
        index_catalog.append(scraper_class(url, driver))

    return index_catalog


def urls_pull_list_collection(index_catalog, catalog):
    """Создаём каталог с перечнем ссылок продуктов."""

    for html in index_catalog:
        catalog.index_catalog_builder(html.soup)


def pages_pull_objects_collection(catalog, delay_time, scraper_class, driver):
    """Создаём массив объектов с данными продуктов."""
    list_to_scrape = []
    total_products = len(catalog.index_catalog)

    counter = 0

    for url in catalog.index_catalog:
        time.sleep(delay_time)
        list_to_scrape.append(scraper_class(url, driver))
        counter += 1
        print(
            f"\rProcessing {counter} of {total_products}", end="", flush=True
        )

    return list_to_scrape


def product_data_builder(json_builder, list_to_scrape):
    """Собираем данные о продуктах в словарь."""

    for page in list_to_scrape:
        json_builder.collect_product_content(page.soup)


def json_generator(json_builder):
    """Создаём JSON фаил на основе данных словаря."""
    with open("leroymerlin_data.json", "w", encoding="utf-8") as outfile:
        json.dump(
            json_builder.product_file, outfile, indent=4, ensure_ascii=False
        )


def main():
    """Основной драйвер проекта."""

    delay_time: int = 5
    driver = uc.Chrome()

    driver.set_window_size(800, 600)

    source_url = "https://leroymerlin.ru/catalogue/parketnye-laki/"

    total_pages, index_catalog = initial_object_collection(source_url, driver)

    full_catalog = urls_pull_object_collection(
        total_pages, delay_time, source_url, index_catalog, Scraper, driver
    )

    catalog = Catalog()

    urls_pull_list_collection(full_catalog, catalog)

    list_to_scrape = pages_pull_objects_collection(
        catalog, delay_time, Scraper, driver
    )

    json_builder = JsonBuilder()

    product_data_builder(json_builder, list_to_scrape)

    json_generator(json_builder)

    driver.close()
    driver.quit()

    print("\rДанные сохранены в .json фаил.")


if __name__ == "__main__":
    main()
