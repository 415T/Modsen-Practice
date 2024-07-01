from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import os

def get_edge_driver_path():
    possible_paths = [
        'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedgedriver.exe',
        'C:\\Program Files\\Microsoft\\Edge\\Application\\msedgedriver.exe',
        '/usr/local/bin/msedgedriver',
        '/usr/bin/msedgedriver'
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

if __name__ == '__main__':
    edge_driver_path = get_edge_driver_path()

    if edge_driver_path:
        # Если драйвер найден, используем его
        service = Service(edge_driver_path)
    else:
        # Если драйвер не найден, загружаем его с помощью webdriver-manager
        service = Service(EdgeChromiumDriverManager().install())

    driver = webdriver.Edge(service=service)

    try:
        driver.get('https://example.com')

        # Устанавливаем значение в cookie
        driver.add_cookie({'name': 'myCookie', 'value': 'myValue'})

        # Получаем значение из cookie
        cookie_value = driver.get_cookie('myCookie')
        print(f'Value from cookie: {cookie_value["value"]}')

        # Удаляем значение из cookie
        driver.delete_cookie('myCookie')

        # Проверяем, что значение удалено
        cookie_value_after_removal = driver.get_cookie('myCookie')
        print(f'Value after removal from cookie: {cookie_value_after_removal}')
    finally:
        input("Press Enter to close the browser and end the program...")
        driver.quit()
