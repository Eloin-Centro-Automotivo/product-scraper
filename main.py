import os
from dotenv import load_dotenv
from selenium.webdriver.remote.webelement import WebElement
from tqdm import tqdm

from browser_automation import BrowserAutomation
from product_database import ProductDatabase
from sampel_product_scraper import SampelProductScraper
from selenium.webdriver.common.by import By

load_dotenv()

cnpj = os.getenv('SKY_PECAS_CNPJ')
username = os.getenv('SKY_PECAS_USERNAME')
password = os.getenv('SKY_PECAS_PASSWORD')

database = ProductDatabase()
database.connect()

browser = BrowserAutomation()

browser.open_new_tab()
browser.login_to_sky_pecas(cnpj, username, password)
browser.switch_to_first_tab()

site_product_codes: list[str] = browser.fetch_product_codes()
new_product_codes: list[str] = database.get_codes_to_save(site_product_codes)

print(database.get_product_count())

# new_product_codes = ['SK368'] # LISTA DE PRODUTOS QUE DAO ERRO
progress_bar = tqdm(new_product_codes, desc="Processing products", unit="product")

for code in progress_bar:
    print(f'codigo atual: {code}')

    browser.open_url('https://catalogo.sampel.com.br/sampel')
    browser.search_product_by_code(code, 'search')

    total_pages: int = browser.get_total_pages('ul.pagination.green') + 1

    for page in range(1, total_pages):
        browser.open_url(f'https://catalogo.sampel.com.br/sampel/produtos/{page}?s={code}&data=&list=')

        product_code_elements: list[WebElement] = browser.safe_get_elements('span.btn-light.border-0')

        for product_code_element in product_code_elements:
            product_code_text = product_code_element.text.strip()

            if product_code_text == code:
                product_link_element = product_code_element.find_element(By.XPATH, './ancestor::div[@class="product-item item list w-100"]//a[@class="green-b-l"]')
                product_url = product_link_element.get_attribute('href')
                browser.open_url(product_url)
                break
        break

    soup = browser.get_soup()
    product_scraper = SampelProductScraper(soup)

    product = product_scraper.create_product(code)
    product.price = browser.get_price(code, 'SAMPEL')

    database.insert_product(product)

browser.quit()

# register_products_on_vip(database)

database.disconnect()
