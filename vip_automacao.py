import time
import pyautogui
from tqdm import tqdm


def register_products_on_vip(database):
    green = "\033[92m"
    reset = "\033[0m"

    products = database.get_products_not_registered_vip()

    pyautogui.doubleClick(39, 540)  # clicar no icone da area de trabalho
    time.sleep(120)  # esperar o sistema abrir
    pyautogui.click(777, 343)  # clicar no campo para inserir a senha
    pyautogui.typewrite('balcao')  # digitar a senha
    pyautogui.click(795, 374)  # clicar para abrir o sistema
    time.sleep(20)  # esperar o sistema abrir
    pyautogui.click(295, 63)  # botao produto
    time.sleep(15)

    half_second = 0.5
    one_second = 1
    two_seconds = 2
    five_seconds = 5

    for product in tqdm(products, desc="Processing products", unit="product"):
        pyautogui.click(278, 680)  # botao novo
        time.sleep(4)

        # Descricao produto
        pyautogui.click(574, 193)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        pyautogui.typewrite('teste')
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        pyautogui.typewrite(product['description'])
        time.sleep(half_second)

        # Campo complemento
        pyautogui.click(629, 196)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        pyautogui.typewrite('')
        time.sleep(half_second)

        # Campo descricao NF
        pyautogui.click(833, 196)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        pyautogui.typewrite(product['description'])
        time.sleep(half_second)

        # Campo marca
        pyautogui.click(891, 319)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        pyautogui.typewrite('85')
        pyautogui.press('enter')
        time.sleep(half_second)

        # Campo Subgrupo
        pyautogui.click(406, 323)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        pyautogui.typewrite('4')
        pyautogui.press('enter')
        time.sleep(half_second)

        # Campo grupo
        pyautogui.click(677, 318)
        time.sleep(one_second)
        pyautogui.click(492, 187)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        pyautogui.typewrite('2')
        time.sleep(half_second)
        pyautogui.press('enter')
        time.sleep(half_second)
        pyautogui.press('enter')
        time.sleep(one_second)

        # Campo codigo
        pyautogui.click(413, 421)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        pyautogui.typewrite(product['code'])
        time.sleep(half_second)

        # Campo aplicacao
        pyautogui.click(499, 565)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        pyautogui.typewrite(product['application'])
        time.sleep(half_second)

        # Campo Prox ->
        pyautogui.click(304, 686)
        time.sleep(one_second)

        # Campo Salvar
        pyautogui.click(304, 686)
        time.sleep(one_second)

        # Caixa de atencao, sim
        pyautogui.click(844, 426)
        time.sleep(two_seconds)

        # Cadastro de fornecedor, salvar
        pyautogui.click(998, 493)
        time.sleep(two_seconds)

        # Foto
        pyautogui.click(590, 146)
        time.sleep(half_second)

        pyautogui.click(293, 350)
        time.sleep(two_seconds)

        pyautogui.click(374, 653)
        time.sleep(one_second)

        pyautogui.click(708, 482)
        time.sleep(one_second)

        pyautogui.click(665, 421)
        pyautogui.typewrite(product['image'])
        time.sleep(one_second)

        pyautogui.click(965, 413)
        time.sleep(two_seconds)

        pyautogui.click(578, 519)
        time.sleep(five_seconds)

        pyautogui.click(1085, 41)
        time.sleep(one_second)

        pyautogui.click(696, 401)

        database.cursor.execute(
            'UPDATE products SET is_registered_vip = 1 WHERE code = ?',
            (product['code'],)
        )
        database.conn.commit()
        print(f'{green}Product: {product['code']} saved successfully{reset}')

        time.sleep(2.5)


# Mostra as coordenadas do mouse quando ele é movido
try:
    while True:
        x, y = pyautogui.position()
        print(f'Posição do mouse: ({x}, {y})', end='\r')
except KeyboardInterrupt:
    print('\nEncerrado.')
