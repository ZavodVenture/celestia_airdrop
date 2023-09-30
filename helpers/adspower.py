import requests
from time import sleep
from entities import Error, Proxy
from threading import Lock
import os
import re

API_URl = 'http://localhost:50325/'

lock = Lock()


def check_adspower():
    try:
        lock.acquire()
        requests.get(API_URl + 'status').json()
        sleep(1)
        lock.release()
    except Exception as e:
        lock.release()
        return Error('Connection error', 'API недоступен. Проверьте, запущен ли AdsPower', e)
    else:
        return True


def get_group_id(group_name):
    args = {
        'group_name': group_name
    }

    try:
        lock.acquire()
        r = requests.get(API_URl + 'api/v1/group/list', params=args).json()
        sleep(1)
        lock.release()
    except Exception as e:
        lock.release()
        return Error('Getting group error', 'Не удалось узнать, существует ли группа', e)
    else:
        if r['code'] != 0:
            return Error('Getting group error', r['msg'])
        else:
            if r['data']['list']:
                return r['data']['list'][0]['group_id']
            else:
                return None


def create_group(name):
    try:
        lock.acquire()
        r = requests.post(API_URl + 'api/v1/group/create', json={'group_name': name}).json()
        sleep(1)
        lock.release()
    except Exception as e:
        lock.release()
        return Error('Group creation error', 'Возникла ошибка при отправке запроса AdsPower', e)
    else:
        if r['code'] != 0:
            return Error('Group creation error', r["msg"])
        else:
            return r['data']['group_id']


def create_profile(proxy: Proxy = None, group_id='0'):
    if proxy:
        account_data = {
            'group_id': group_id,
            'user_proxy_config': {
                'proxy_soft': 'other',
                'proxy_type': 'socks5',
                'proxy_host': proxy.ip,
                'proxy_port': proxy.port,
                'proxy_user': proxy.login,
                'proxy_password': proxy.password
            }
        }
    else:
        account_data = {
            'group_id': group_id,
            'user_proxy_config': {
                'proxy_soft': 'no_proxy'
            }
        }

    try:
        lock.acquire()
        r = requests.post(API_URl + 'api/v1/user/create', json=account_data).json()
        sleep(1)
        lock.release()
    except Exception as e:
        lock.release()
        return Error('Connection error', 'Возникла ошибка при отправке запроса AdsPower', e)
    else:
        if r['code'] != 0:
            return Error('Profile creation error', r['msg'])
        else:
            return r['data']['serial_number']


def run_profile(serial_number):
    args = {
        'serial_number': serial_number,
        'ip_tab': 0
    }
    try:
        lock.acquire()
        r = requests.get(API_URl + 'api/v1/browser/start',  params=args).json()
        sleep(1)
        lock.release()
    except Exception as e:
        lock.release()
        return Error('Connection error', 'Возникла ошибка при отправке запроса AdsPower', e)
    else:
        if r['code'] != 0:
            return Error('Profile launching error', r['msg'])
        else:
            ws = r["data"]["ws"]["selenium"]
            driver_path = r["data"]["webdriver"]
            return ws, driver_path


def close_profile(serial_number):
    args = {
        'serial_number': serial_number
    }

    try:
        lock.acquire()
        requests.get(API_URl + 'api/v1/browser/stop', params=args)
        sleep(1)
        lock.release()
    except:
        lock.release()
        pass


def delete_profile(serial_number):
    args = {
        'serial_number': serial_number
    }

    try:
        lock.acquire()
        r = requests.get(API_URl + 'api/v1/user/list', params=args).json()
        sleep(1)
        lock.release()
    except:
        lock.release()
        return

    if not r['data']['list']:
        return

    user_id = r['data']['list'][0]['user_id']

    try:
        lock.acquire()
        requests.post(API_URl + 'api/v1/user/delete', json={'user_ids': [user_id]})
        sleep(1)
        lock.release()
    except:
        lock.release()
        pass


def bypass_metamask():
    for disk in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
        try:
            os.listdir(f'{disk}:\.ADSPOWER_GLOBAL')
        except FileNotFoundError:
            continue
        else:
            adspower_path = f'{disk}:\.ADSPOWER_GLOBAL'
            break
    else:
        return False

    if 'extension' in os.listdir(adspower_path):
        extension_folders = os.listdir(f'{adspower_path}\\extension')

        extension_changed = False

        for extension in extension_folders:
            current_extension_folders = os.listdir(f'{adspower_path}\\extension\\{extension}')

            for folder in current_extension_folders:
                if not os.path.isdir(f'{adspower_path}\\extension\\{extension}\\{folder}'):
                    continue

                if 'runtime-lavamoat.js' in os.listdir(f'{adspower_path}\\extension\\{extension}\\{folder}'):
                    lavamoat_path = f'{adspower_path}\\extension\\{extension}\\{folder}\\runtime-lavamoat.js'
                    with open(lavamoat_path, encoding='utf-8') as file:
                        text = file.read()
                        file.close()
                    with open(lavamoat_path, 'w', encoding='utf-8') as file:
                        replaced_text = re.sub(r'} = {"scuttleGlobalThis":\{.*}',
                                               '} = {"scuttleGlobalThis":{"enabled":false,"scuttlerName":"SCUTTLER","exceptions":[]}}',
                                               text)
                        file.write(replaced_text)
                        file.close()

                    extension_changed = True

        if not extension_changed:
            return False

    if 'ext' in os.listdir(adspower_path):
        ext_folders = os.listdir(f'{adspower_path}\\ext')

        extension_changed = False

        for extension in ext_folders:
            if not os.path.isdir(f'{adspower_path}\\ext\\{extension}'):
                continue

            if 'runtime-lavamoat.js' in os.listdir(f'{adspower_path}\\ext\\{extension}'):
                lavamoat_path = f'{adspower_path}\\ext\\{extension}\\runtime-lavamoat.js'
                with open(lavamoat_path, encoding='utf-8') as file:
                    text = file.read()
                    file.close()
                with open(lavamoat_path, 'w', encoding='utf-8') as file:
                    replaced_text = re.sub(r'} = {"scuttleGlobalThis":\{.*}',
                                           '} = {"scuttleGlobalThis":{"enabled":false,"scuttlerName":"SCUTTLER","exceptions":[]}}',
                                           text)
                    file.write(replaced_text)
                    file.close()
                extension_changed = True

        if not extension_changed:
            return False

    return True
