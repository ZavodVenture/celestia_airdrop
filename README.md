# Celestia Airdrop

Этот скрипт поможет проверить наличие дропа и сделать клейм на любом количестве аккаунтов.

***Клеймим на адрес Celestia, полученный из сидки метамаска.***

***При работе с прокси могут быть проблемы, так как для этого дропа требуются весьма специфичные прокси, которые тяжело найти с приемлемой для автоматизации скоростью.***
## Подготовка AdsPower

Для работы скрипт использует анти-детект браузер **AdsPower**, поэтому первым делом нужно создать аккаунт **[здесь](https://app.adspower.com/registration)**.

![image](https://github.com/ZavodVenture/celestia_airdrop/assets/42314185/ed6a1721-7aee-4bc3-bf8f-3b6c97fef3fb)

Покупать подписку не нужно, в AdsPower есть бесплатный пробный период на три дня. Сразу после регистрации активируем его:

![image](https://github.com/ZavodVenture/celestia_airdrop/assets/42314185/2ccf233b-50f8-4e25-9470-e8d36e518422)
![image](https://github.com/ZavodVenture/celestia_airdrop/assets/42314185/3f2cb736-5325-4d14-993c-ad66732a4402)

Следующим этапом необходимо установить и включить два расширения для Chrome: **MetaMask** и **Keplr**. Оба необходимы для получения дропа.

![image](https://github.com/ZavodVenture/celestia_airdrop/assets/42314185/7cf840fc-db9f-4e89-b782-bf48e2f0d696)
![image](https://github.com/ZavodVenture/celestia_airdrop/assets/42314185/533f3f5a-ae2e-4a94-b50c-40f95ad76cdb)
![image](https://github.com/ZavodVenture/celestia_airdrop/assets/42314185/0053c602-6a1a-4ee7-b514-2761126d03f9)

URL расширений:
1. **MetaMask** - https://chrome.google.com/webstore/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn
2. **Kelpr** - https://chrome.google.com/webstore/detail/keplr/dmkamcknogkgcdfhhbddcghachkejeap

После установки расширений **[устанавливаем](https://www.adspower.com/download)** клиент **AdsPower** для Вашей системы, запускаем его, входим в аккаунт и забываем о нём.

## Подготовка входных данных

Скрипт может работать как с прокси, так и без них. Входные данные в этих двух случаях будут отличаться:

1. С прокси: `сид-фраза Metamask:адрес кошелька metamask:ip:port:user:password`
2. Без прокси: `сид-фраза Metamask:адрес кошелька metamask`

Скрипт принимает только прокси socks5.

Пример строки файла входных данных:

1. С прокси: `gesture cat wrestle wave power high steak ocean marble output black priority:0x39cc818a6c053CEae177EC76971c74bFcF5f0afD:153.51.21.14:7565:admin:123123`
2. Без прокси: `choice industry man brand element shrimp connect treat merit enforce quality elbow:0xe3dcF6f5Fd2252Ad2EFCC776138EEe273e327Bf2`

Входной файл скрипта должен состоять из любого количества строк такого формата.

## Загрузка скрипта

Здесь тоже два варианта:
1. Вы можете установить python 3.8 на Ваш ПК, загрузить исходный код скрипта, установить зависимости и запустить скрипт
2. ...Или, если Вы пользуетесь Windows, доверяете **_Заводу_** и не хотите тратить время на вышеперечисленные шаги, загрузить скомпилированный из исходного кода exe файл в [данном репозитории](https://github.com/ZavodVenture/celestia_airdrop_compilled) и запустить скрипт из него :) Скрипт может помечаться, как троян, так как взаимодействует с файлами расширения MetaMask для отключения защиты от автоматизации, это нормально, троянов здесь нет.

Загрузить код ниже можно вот так. Ниже в этом репозитории расписаны все шаги запуска исходного кода.

![image](https://github.com/ZavodVenture/celestia_airdrop/assets/42314185/a28f6257-bcd2-48d3-98bd-25c7298ef744)

## Установка зависимостей для исходного кода

Для начала нужно установить python 3.8 ([инсталлятор для Mac](https://www.python.org/ftp/python/3.8.0/python-3.8.0-macosx10.9.pkg), [инсталлятор для Windows](https://www.python.org/ftp/python/3.8.0/python-3.8.0-amd64.exe)).

***Работа скрипта не проверялась на Mac OS, поэтому если что-то не будет работать, рекомендую арендовать сервер на Windows и запускать скрипт на нём.***

При установке необходимо поставить галочку `Add Python 3.8 to PATH`, если она есть.

После установки python 3.8 загружаем исходный код скрипта и распаковываем в любую папку и открываем её.

В папке есть файл `install_requirements.sh`. Запускаем его. Это установит необходимые для работы скрипта библиотеки.

## Запуск скрипта

Перед запуском скрипта нужно открыть файл config.ini и выбрать необходимые настройки:
1. `threads` - количество одновременно запущенных браузеров. Зависит от мощности ПК, рекомендуется `2`
2. `use_proxy` - использование прокси. `0` - не использовать, `1` - использовать.

Далее, в зависимости от выбранной настройки `use_proxy`, нужно загрузить аккаунты в нужном формате в файл `input.txt`

После этого можно запускать файл `main.py` _(или `main.exe`, если вы выбрали запускать скомпилированный файл)_ и просто ждать. После завершения работы со всеми аккаунтами скрипт запишет лог работы с каждым из них в папку `logs`.