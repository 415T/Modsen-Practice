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

        # Устанавливаем значение в LocalStorage
        script_set = "localStorage.setItem('myNickname', 'Greed;)');"
        driver.execute_script(script_set)

        # Получаем значение из LocalStorage
        script_get = "return localStorage.getItem('myNickname');"
        value = driver.execute_script(script_get)
        print(f'Value from LocalStorage: {value}')

        # Удаляем значение из LocalStorage
        script_remove = "localStorage.removeItem('myNickname');"
        driver.execute_script(script_remove)

        # Проверяем, что значение удалено
        value_after_removal = driver.execute_script(script_get)
        print(f'Value after removal from LocalStorage: {value_after_removal}')
    finally:
        input("Press Enter to close the browser and end the program...")
        driver.quit()
