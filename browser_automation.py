from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm


def parse_product_details(product_text: str) -> dict[str, str]:
    details = {}
    lines = product_text.split('\n')

    for line in lines:
        line = line.strip()

        if line.startswith('Cód. Fáb:'):
            details['code'] = line.replace('Cód. Fáb:', '').strip()

        elif line.startswith('R$'):
            price = line.replace('R$', '').split('/')[0].strip()
            details['price'] = price

    return details


class BrowserAutomation:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 2.5)


    def accept_alert(self) -> None:
        self.wait.until(EC.alert_is_present()).accept()


    def clear_and_send_keys_then_enter(self, value: str, xpath: str) -> None:
        input_value = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        input_value.clear()
        input_value.send_keys(value)
        input_value.send_keys(Keys.ENTER)


    def click_product_by_code(self, target_code: str, css_selector: str) -> None:
        for product_code_element in self.safe_get_elements(css_selector):
            product_code_text = product_code_element.text.strip()

            if product_code_text == target_code:
                product_link_element = self.get_element_by_xpath('./ancestor::div[@class="product-item item list w-100"]//a[@class="green-b-l"]')
                product_link_element.click()
                break


    def fetch_product_codes(self) -> list[str]:
        unique_codes = set()
        carmakers_code: dict[str, list[str]] = self.get_all_carmakers_code()

        for codes in carmakers_code.values():
            unique_codes.update(codes)

        return list(unique_codes)


    def get_all_carmakers_code(self) -> dict[str, list[str]]:
        carmakers: list[str] = [
            'Audi', 'Chevrolet', 'Citroen', 'Fiat', 'Ford', 'Honda', 'Hyundai',
            'Nissan', 'Peugeot', 'Renault', 'Toyota', 'Volkswagen'
        ]
        carmakers_code: dict[str, list[str]] = {item: [] for item in carmakers}

        for carmaker in tqdm(carmakers, desc="Processing carmakers", unit="carmaker"):
            self.open_url(f'https://catalogo.sampel.com.br/sampel/produtos?m={carmaker}')
            total_pages: int = self.get_total_pages('ul.pagination.green') + 1

            for page in range(1, total_pages):
                self.open_url(f'https://catalogo.sampel.com.br/sampel/produtos/{page}?m={carmaker}')
                code_elements: list[WebElement] = self.safe_get_elements('span.btn-light.border-0')

                for code_element in code_elements:
                    code: str = code_element.text.strip()

                    if ' ' not in code:
                        carmakers_code[carmaker].append(code)

        return carmakers_code


    def get_element_by_css(self, css_selector: str) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))


    def get_element_by_id(self, id: str) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located((By.ID, id)))


    def get_element_by_xpath(self, xpath: str) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))


    def get_elements_by_css(self, css_selector: str) -> list[WebElement]:
        return self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, css_selector)))


    def handle_product_not_found_popup(self) -> None:
        try:
            button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.swal2-confirm.swal2-styled')))

            if button:
                button.click()

        except Exception:
            pass


    def get_price(self, code: str, brand: str) -> str:
        self.switch_to_second_tab()
        self.select_brand(brand, '//*[@id="select2-inpMarca-container"]', '//*[@id="body"]/span/span/span[1]/input')
        self.clear_and_send_keys_then_enter(code, '//*[@id="inpCodigo"]')
        self.handle_product_not_found_popup()

        price: str = '0'
        product_elements: list[WebElement] = self.safe_get_elements('div.bx_produto')

        for product in product_elements:
            product_details: dict[str, str] = parse_product_details(product.text)

            if product_details['code'] == code:
                price = product_details['price']
                break

        self.switch_to_first_tab()
        return price


    def get_soup(self) -> BeautifulSoup:
        html: str = self.driver.page_source
        return BeautifulSoup(html, 'html.parser')


    def get_total_pages(self, css_selector: str) -> int:
        ul_element: WebElement = self.get_element_by_css(css_selector)
        li_elements: list[WebElement] = ul_element.find_elements(By.TAG_NAME, 'li')
        last_li_element: WebElement = li_elements[-1]
        a_tag: WebElement = last_li_element.find_element(By.TAG_NAME, 'a')
        total_pages: str = a_tag.text.strip()
        return int(total_pages)


    def login_to_sky_pecas(self, cnpj: str, user: str, password: str) -> None:
        self.open_url('https://novo.enviapecas.com.br/usuario/login')
        self.wait_for_and_send_keys(cnpj, '//*[@id="txtCNPJCPF"]')
        self.wait_for_and_send_keys(user, '//*[@id="bx_login"]/form/p[2]/input')
        self.wait_for_and_send_keys(password, '//*[@id="bx_login"]/form/p[3]/input')
        self.wait_and_click('//*[@id="btnEntrar"]')
        self.accept_alert()
        self.wait_and_click('//*[@id="btnEntrar"]')
        # self.wait_and_click('//*[@id="bx_modal"]/a')


    def open_new_tab(self) -> None:
        self.driver.execute_script("window.open('');")
        self.switch_to_second_tab()


    def open_url(self, url: str) -> None:
        self.driver.get(url)


    def quit(self) -> None:
        self.driver.quit()


    def safe_get_elements(self, css_selector: str) -> list[WebElement]:
        try:
            return self.get_elements_by_css(css_selector)
        except TimeoutException:
            return []


    def search_product_by_code(self, code: str, id_element: str) -> None:
        search_input = self.get_element_by_id(id_element)
        search_input.clear()
        search_input.send_keys(code)
        search_input.send_keys(Keys.ENTER)


    def select_brand(self, brand: str, container_xpath: str, input_xpath: str) -> None:
        brand_container = self.wait.until(EC.visibility_of_element_located((By.XPATH, container_xpath)))

        if brand_container.text == 'Marcas':
            brand_container.click()
            self.send_keys_and_press_enter(brand, input_xpath)


    def send_keys_and_press_enter(self, value: str, xpath: str) -> None:
        input_value = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        input_value.send_keys(value)
        input_value.send_keys(Keys.ENTER)


    def switch_to_first_tab(self) -> None:
        self.driver.switch_to.window(self.driver.window_handles[0])


    def switch_to_second_tab(self) -> None:
        self.driver.switch_to.window(self.driver.window_handles[1])


    def wait_and_click(self, xpath: str) -> None:
        button = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        button.click()


    def wait_for_and_send_keys(self, value: str, xpath: str) -> None:
        input_value = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        input_value.send_keys(value)
