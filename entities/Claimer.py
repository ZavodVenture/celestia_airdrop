from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from entities import Error
import sys
import os
from time import sleep


class Claimer:
    driver: webdriver.Chrome = None

    def __init__(self, seed_phrase, address, ws, driver_path):
        self.seed_phrase = seed_phrase
        self.address = address
        self.ws = ws
        self.driver_path = driver_path

    def get_exts(self):
        self.driver.get('chrome://extensions/')

        script = '''ext_manager = document.getElementsByTagName('extensions-manager')[0].shadowRoot;
        item_list = ext_manager.getElementById('items-list').shadowRoot;
        container = item_list.getElementById('container');
        extension_list = container.getElementsByClassName('items-container')[1].getElementsByTagName('extensions-item');
        
        var extensions = [];
        
        for (i = 0; i < extension_list.length; i++) {
            console.log(extension_list[i]);
            name = extension_list[i].shadowRoot.getElementById('name').textContent;
            id = extension_list[i].id;
            extensions.push({'id': id, 'name': name});
        }
        
        return extensions;'''

        extension_list = self.driver.execute_script(script)

        metamask_id = None
        keplr_id = None

        for i in extension_list:
            if 'MetaMask' in i['name']:
                metamask_id = i['id']
            elif 'Keplr' in i['name']:
                keplr_id = i['id']

        return metamask_id, keplr_id

    def enter_metamask(self, ext_id):
        try:
            self.driver.get(f'chrome-extension://{ext_id}/home.html#onboarding/welcome')
            try:
                WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.XPATH, '//div[@class="loading-overlay"]')))
            except:
                pass
            else:
                try:
                    WebDriverWait(self.driver, 30).until_not(ec.presence_of_element_located((By.XPATH, '//div[@class="loading-overlay"]')))
                except:
                    return Error('Вход в метамаск', 'Метамаску не удалось подключиться к сети. Проблема в прокси.')

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="onboarding__terms-checkbox"]'))).click()  # Чекбокс правил
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/ul/li[3]/button'))).click()  # Кнопка импорта
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div/button[1]'))).click()  # Кнопка согласия

            WebDriverWait(self.driver, 15).until(ec.presence_of_element_located((By.XPATH, '//input[@type="password"]')))

            fields = self.driver.find_elements(By.XPATH, '//input[@type="password"]')

            for i in range(len(fields)):
                fields[i].send_keys(self.seed_phrase.split()[i])

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[4]/div/button'))).click()  # Кнопка импорта сидки

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[1]/label/input'))).send_keys('123123123')  # Пароль 123123123
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[2]/label/input'))).send_keys('123123123')  # Повтор пароля

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[3]/label/input'))).click()  # Флажок правил

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/button'))).click()  # Импорт

            sleep(2)
            self.driver.refresh()

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'))).click()  # Got It

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'))).click()  # Ещё кнопка
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'))).click()  # Ещё кнопка

            sleep(1)

            self.driver.get('about:blank')
        except Exception as e:
            e_type, e_obj, e_tb = sys.exc_info()
            filename = os.path.split(e_tb.tb_frame.f_code.co_filename)[1]

            return Error('Вход в метамаск', 'Произошла непредвиденная ошибка', e, filename, e_tb.tb_lineno)

    def enter_keplr(self, ext_id):
        try:
            self.driver.get(f'chrome-extension://{ext_id}/register.html#')

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div/div[3]/div[3]/button'))).click()  # Кнопка импорта
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[2]/div/div/div/div[1]/div/div[5]/button'))).click()  # Кнопка импорта сидки

            WebDriverWait(self.driver, 15).until(ec.presence_of_element_located((By.XPATH, '//input[@type="password"]')))

            inputs = self.driver.find_elements(By.XPATH, '//input[@type="password"]')

            for i in range(len(inputs)):
                inputs[i].send_keys(self.seed_phrase.split(' ')[i])
                sleep(0.1)

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[3]/div/div/form/div[6]/div/button'))).click()  # Кнопка импортна сидки
            sleep(0.1)
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[4]/div/div/form/div/div[1]/div[2]/div/div/input'))).send_keys('1')  # Имя кошелька
            sleep(0.1)
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[4]/div/div/form/div/div[3]/div[2]/div/div/input'))).send_keys('123123123')  # Пароль
            sleep(0.1)
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[4]/div/div/form/div/div[5]/div[2]/div/div/input'))).send_keys('123123123')  # Повтор пароля
            sleep(0.1)

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[4]/div/div/form/div/div[7]/button'))).click()  # Кнопка "дальше"

            WebDriverWait(self.driver, 15).until(ec.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div/div[1]/div[2]/div/div[2]/input'))).send_keys('Celestia')
            sleep(0.1)
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div/div[5]/div[1]/div[2]/div/div/div/div/div'))).click()

            # sleep(0.1)
            # WebDriverWait(self.driver, 15).until(ec.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div/div[1]/div[2]/div/div[2]/input'))).send_keys(Keys.CONTROL, 'a')
            # WebDriverWait(self.driver, 15).until(ec.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div/div[1]/div[2]/div/div[2]/input'))).send_keys(Keys.BACKSPACE)
            # sleep(0.1)
            # WebDriverWait(self.driver, 15).until(ec.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div/div[1]/div[2]/div/div[2]/input'))).send_keys('Cosmos')
            # sleep(0.1)
            # WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div/div[5]/div[1]/div[2]/div/div/div/div/div'))).click()

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div/div[9]/div/button'))).click()  # Сохарняем сети

            self.driver.get('about:blank')
        except Exception as e:
            e_type, e_obj, e_tb = sys.exc_info()
            filename = os.path.split(e_tb.tb_frame.f_code.co_filename)[1]

            return Error('Вход в кеплер', 'Произошла непредвиденная ошибка', e, filename, e_tb.tb_lineno)

    def prepare_webdriver(self):
        try:
            options = Options()
            options.add_experimental_option("debuggerAddress", self.ws)
            service = Service(executable_path=self.driver_path)
            driver = webdriver.Chrome(service=service, options=options)
            self.driver = driver
            self.driver.maximize_window()

            try:
                WebDriverWait(self.driver, 5).until_not(ec.number_of_windows_to_be(1))
            except:
                pass
            else:
                sleep(5)
                self.driver.switch_to.new_window()
                self.driver.get('about:blank')

                main = self.driver.current_window_handle
                windows = self.driver.window_handles
                windows.remove(main)
                for window in windows:
                    self.driver.switch_to.window(window)
                    self.driver.close()

                self.driver.switch_to.window(main)

            metamask_id, keplr_id = self.get_exts()

            if not metamask_id or not keplr_id:
                return Error('Ошибка расширений', 'Не найдены Keplr и Metamask')

            result = self.enter_metamask(metamask_id)

            if isinstance(result, Error):
                return result

            result = self.enter_keplr(keplr_id)

            if isinstance(result, Error):
                return result
        except Exception as e:
            e_type, e_obj, e_tb = sys.exc_info()
            filename = os.path.split(e_tb.tb_frame.f_code.co_filename)[1]

            return Error('Ошибка подготовки драйвера', 'Произошла непредвиденная ошибка', e, filename, e_tb.tb_lineno)

    def check_eligibility(self):
        try:
            self.driver.get('https://genesis.celestia.org/')
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/main/div/div/div/div[1]/div/div/div[2]/div[1]/button'))).click()  # Кнопка Check
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/div[2]/div[2]/div/div[9]/div/label/div'))).click()  # Флажок согласия с правилами
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/div[2]/div[2]/div/div[8]'))).click()  # Кнопка ручного ввода кошелька
            address_input = WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="wallet_address"]')))  # Поле ввода адреса для проверки

            address_input.send_keys(self.address)

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/main/div/div/div/div[2]/div[2]/button'))).click()  # Кнопка проверки

            while 1:
                eligibility_div = WebDriverWait(self.driver, 30).until(ec.presence_of_element_located((By.XPATH, '//div[contains(@class, "eligible")]')))
                if 'captcha' in eligibility_div.find_element(By.XPATH, 'div/div/h5').text:
                    sleep(5)
                    WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/main/div/div/div/div[3]/div[2]/button'))).click()
                    WebDriverWait(self.driver, 30).until_not(ec.presence_of_element_located((By.XPATH, '//div[contains(@class, "eligible")]')))
                    continue
                break

            if 'not-eligible' in eligibility_div.get_attribute('class'):
                return False
            else:
                return True
        except Exception as e:
            e_type, e_obj, e_tb = sys.exc_info()
            filename = os.path.split(e_tb.tb_frame.f_code.co_filename)[1]

            return Error('Проверка доступности дропа', 'Произошла непредвиденная ошибка', e, filename, e_tb.tb_lineno)

    def claim(self):
        try:
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/main/div/div/div/div[3]/div/div[2]/button'))).click()  # Кнопка коннекта кошелька
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/main/div/div/div/div[2]/div[2]/div/div[3]/div/label/div'))).click()  # Флажок правил
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/div/div/div[2]'))).click()  # Кнопка выбора кошелька
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[2]/div[3]'))).click()  # Кнопка выбора метыча

            WebDriverWait(self.driver, 15).until(ec.number_of_windows_to_be(2))

            original_window = self.driver.current_window_handle
            windows = self.driver.window_handles
            windows.remove(original_window)
            self.driver.switch_to.window(windows[0])

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div/div/div[3]/div[2]/footer/button[2]'))).click()  # Кнопка "Далее" в метамаске
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div/div/div[3]/div[2]/footer/button[2]'))).click()  # Кнопка "Подключиться" в метамаске

            sleep(3)

            self.driver.switch_to.window(original_window)
            WebDriverWait(self.driver, 15).until(ec.number_of_windows_to_be(2))

            original_window = self.driver.current_window_handle
            windows = self.driver.window_handles
            windows.remove(original_window)
            self.driver.switch_to.window(windows[0])

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div/div/div[4]/footer/button[2]'))).click()  # Кнопка подписи в метамаске
            WebDriverWait(self.driver, 15).until(ec.number_of_windows_to_be(1))
            self.driver.switch_to.window(original_window)

            try:
                WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.XPATH, '//div[contains(@class, "already_claimed")]')))
            except:
                pass
            else:
                minimum_tia = self.driver.find_element(By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/main/div/div/div/div/div/div[1]/p[4]').text
                address = self.driver.find_element(By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/main/div/div/div/div/div/div[1]/p[2]').text
                return minimum_tia, address

            sleep(3)

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div[2]/div/div/div/div/div[3]/div[1]/button'))).click()  # Крестик на окошке

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/main/div/div/div/div[3]/div/div[2]/div[2]/div/button'))).click()  # Кнопка клейма

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/main/div/div/div/div[2]/div[4]/div/label/div'))).click()  # Кнопка принятия правил клейма
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/main/div/div/div/div[2]/div[2]/button[1]'))).click()  # Кнопка импорта адреса с кошелька

            WebDriverWait(self.driver, 15).until(ec.number_of_windows_to_be(2))

            original_window = self.driver.current_window_handle
            windows = self.driver.window_handles
            windows.remove(original_window)
            self.driver.switch_to.window(windows[0])

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div/div/div/form/div[3]/div/div/button'))).click()  # Кнопка Approve в Keplr
            WebDriverWait(self.driver, 15).until(ec.number_of_windows_to_be(1))
            self.driver.switch_to.window(original_window)

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/main/div/div/div/div[2]/div[3]/button'))).click()  # Кнопка клейма

            WebDriverWait(self.driver, 15).until(ec.presence_of_element_located((By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/main/div/div/div/div[1]/div/h3/div[1]/div[text()="Genesis address submitted"]')))

            minimum_tia = self.driver.find_element(By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/main/div/div/div/div[2]/div[1]/div/div[2]/div[2]/div').text
            address = self.driver.find_element(By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/main/div/div/div/div[2]/div[1]/div/div[1]/div[2]/div').text

            return minimum_tia, address
        except Exception as e:
            e_type, e_obj, e_tb = sys.exc_info()
            filename = os.path.split(e_tb.tb_frame.f_code.co_filename)[1]

            return Error('Ошибка клейма', 'Произошла непредвиденная ошибка', e, filename, e_tb.tb_lineno)
