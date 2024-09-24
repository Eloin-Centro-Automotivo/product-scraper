import os
import sqlite3

class ProductDatabase:
    def __init__(self, db_name='products.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None


    def check_database_exists(self):
        return os.path.exists(self.db_name)


    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()


    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            code TEXT PRIMARY KEY NOT NULL,
            description TEXT NOT NULL,
            image TEXT NOT NULL,
            application TEXT NOT NULL,
            is_registered_vip BOOLEAN NOT NULL DEFAULT 0,
            price TEXT
        )
        ''')
        self.conn.commit()


    def disconnect(self):
        if self.conn:
            self.conn.close()


    @staticmethod
    def filter_new_codes(existing_codes, site_codes):
        return list(set(site_codes) - set(existing_codes))


    def get_all_codes(self):
        self.cursor.execute('SELECT code FROM products')
        codes = self.cursor.fetchall()
        return [code[0] for code in codes]


    def get_codes_to_save(self, site_codes) -> list[str]:
        if self.check_database_exists():
            existing_codes = self.get_all_codes()
            return self.filter_new_codes(existing_codes, site_codes)
        else:
            return site_codes


    def get_products_not_registered_vip(self):
        self.cursor.execute('''SELECT * FROM products WHERE is_registered_vip = 0''')

        products = self.cursor.fetchall()
        return [
            {
                'code': row[0],
                'description': row[1],
                'image': row[2],
                'application': row[3],
                'is_registered_vip': row[4],
                'price': row[5]
            }
            for row in products
        ]


    def get_product_count(self):
        self.cursor.execute('SELECT COUNT(*) FROM products')
        count = self.cursor.fetchone()[0]
        return count


    def insert_product(self, product) -> None:
        self.cursor.execute('''
            INSERT INTO products (code, description, image, application, is_registered_vip, price) 
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (product.code, product.description, product.image,
             product.application, product.is_registered_vip, product.price)
        )
        self.conn.commit()

        if product.price == '0':
            print(f'\n\033[93mProduct: {product.code} | Description: {product.description} | Price: {product.price} is unavailable for purchase\033[0m')
        else:
            print(f'\n\033[92mProduct: {product.code} | Description: {product.description} | Price: {product.price} saved successfully\033[0m')
