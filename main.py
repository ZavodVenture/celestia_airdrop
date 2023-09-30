import os.path
from entities import Claimer, Error, Proxy, Account
from helpers import adspower
from configparser import ConfigParser
from colorama import Fore, init
from progress.bar import Bar
from typing import List
from threading import Thread

config = ConfigParser()
config.read('config.ini')

max_threads = int(config['settings']['threads'])
active_threads = 0


def init_exit():
    input('Нажмите Enter, чтобы выйти...')
    exit()


def worker(account: Account, bar: Bar):
    global active_threads

    log = ''

    log += 'Создание профиля AdsPower...\n'

    profile_id = adspower.create_profile(proxy=account.proxy)

    if isinstance(profile_id, Error):
        log += str(profile_id)
        bar.next()
        active_threads -= 1
        with open(f'logs/{account.address}.txt', 'w', encoding='utf-8') as file:
            file.write(log)
            file.close()
        return

    log += f'Создан профиль {profile_id} с прокси {account.proxy}\n'

    log += f'Запуск профиля...\n'

    result = adspower.run_profile(profile_id)

    if isinstance(result, Error):
        log += str(result)
        adspower.delete_profile(profile_id)
        bar.next()
        active_threads -= 1
        with open(f'logs/{account.address}.txt', 'w', encoding='utf-8') as file:
            file.write(log)
            file.close()
        return

    ws, driver_path = result

    log += f'Профиль запущен!\n'
    log += f'Подготовка браузера...\n'

    claimer = Claimer(account.seed, account.address, ws, driver_path)

    result = claimer.prepare_webdriver()

    if isinstance(result, Error):
        log += str(result)
        adspower.close_profile(profile_id)
        adspower.delete_profile(profile_id)
        bar.next()
        active_threads -= 1
        with open(f'logs/{account.address}.txt', 'w', encoding='utf-8') as file:
            file.write(log)
            file.close()
        return

    log += f'Подготовка завершена!\n'

    log += f'Проверка доступности дропа...\n'

    result = claimer.check_eligibility()

    if isinstance(result, Error):
        log += str(result)
        adspower.close_profile(profile_id)
        adspower.delete_profile(profile_id)
        bar.next()
        active_threads -= 1
        with open(f'logs/{account.address}.txt', 'w', encoding='utf-8') as file:
            file.write(log)
            file.close()
        return

    if not result:
        log += f'Дроп не доступен на кошельке {account.address}'
        adspower.close_profile(profile_id)
        adspower.delete_profile(profile_id)
        bar.next()
        active_threads -= 1
        with open(f'logs/{account.address}.txt', 'w', encoding='utf-8') as file:
            file.write(log)
            file.close()
        return

    log += f'Дроп доступен!\n'
    log += 'Клеймим...\n'

    result = claimer.claim()

    if isinstance(result, Error):
        log += str(result)
        adspower.close_profile(profile_id)
        adspower.delete_profile(profile_id)
        bar.next()
        active_threads -= 1
        with open(f'logs/{account.address}.txt', 'w', encoding='utf-8') as file:
            file.write(log)
            file.close()
        return

    minimum_tia, celestia_address = result

    log += f'Заклеймили минимум {minimum_tia} TIA на адрес {celestia_address}! Сидка та же, что и от {account.address}'

    adspower.close_profile(profile_id)
    adspower.delete_profile(profile_id)

    with open(f'logs/{account.address}.txt', 'w', encoding='utf-8') as file:
        file.write(log)
        file.close()

    bar.next()

    active_threads -= 1


def main():
    print(f'Проверка и настройка перед запуском...\n')

    if isinstance(adspower.check_adspower(), Error):
        print(f'{Fore.RED}Не удалось подключиться к AdsPower. Проверьте, запущен ли он.{Fore.RESET}\n')
        init_exit()

    if isinstance(adspower.bypass_metamask(), Error):
        print(f'{Fore.RED}Не удалось изменить расширение MetaMask. Проверьте, установлено ли оно{Fore.RESET}\n')
        init_exit()

    if not os.path.exists('input.txt'):
        print(f'{Fore.RED}Файл input.txt не найден{Fore.RESET}\n')
        init_exit()

    data: List[str] = open('input.txt').read().split('\n')

    if not data[-1]:
        data = data[:-1]

    for i in range(len(data)):
        split = data[i].split(':')

        if int(config['settings']['use_proxy']):
            if len(split) != 6:
                print(f'{Fore.RED}В входном файле неверно записана {i + 1} строка{Fore.RESET}\n')
                init_exit()
        else:
            if len(split) != 2:
                print(f'{Fore.RED}В входном файле неверно записана {i + 1} строка{Fore.RESET}\n')
                init_exit()
        data[i] = Account(*split)

    print(f'{Fore.GREEN}Проверка завершена! Начинаем клейм...{Fore.RESET}\n')

    bar = Bar(max=len(data))
    bar.start()

    threads = [Thread(target=worker, args=(i, bar)) for i in data]

    global active_threads

    for thread in threads:
        while active_threads >= max_threads:
            continue

        active_threads += 1
        thread.start()

    while active_threads != 0:
        continue

    bar.finish()

    print(f'\n{Fore.GREEN}Работа скрипта завершена! Результаты находятся в папке logs.{Fore.RESET}\n')
    init_exit()


if __name__ == '__main__':
    init()
    main()
