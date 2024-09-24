from product import Product


def get_year(year_tag) -> str:
    year: str = ''

    if year_tag:
        year = year_tag.text.strip()
    return year


def get_model(model_tag) -> str:
    model = ''

    if model_tag:
        model = model_tag.text.strip()
    return model


class SampelProductScraper:
    def __init__(self, soup) -> None:
        self.soup = soup


    def get_description(self) -> str:
        description_element = self.soup.find("h1", class_="title text-uppercase")
        return description_element.text.strip() if description_element else 'No description'


    def get_image(self) -> str:
        element = self.soup.find("a", class_="gallery-photo photo-1 selected")
        return element.get('href') if element else 'No image'


    def get_application(self) -> str:
        data = []
        current_brand = None

        for row in self.soup.find_all('tr'):
            if 'green-link' in row.get('class', []):
                current_brand = row.find('strong').text.strip()
            elif current_brand and row.find('td', class_='text-uppercase models'):
                tds = row.find_all('td')
                year_tag = tds[1]
                model_tag = tds[0].find('b')

                data.append({
                    'brand': current_brand,
                    'model': get_model(model_tag),
                    'year': get_year(year_tag)
                })

        output = f"{'Marca':<20} {'Modelo':<10} {'Ano':<15}\n"
        for item in data:
            output += f"{item['brand']:<20} {item['model']:<10} {item['year']:<15}\n"

        return output


    def create_product(self, code) -> Product:
        product = Product()
        product.code = code
        product.description = self.get_description()
        product.image = self.get_image()
        product.application = self.get_application()
        product.is_registered_vip = False
        return product
