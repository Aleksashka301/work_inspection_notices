# Work inspection notices
## Описание
 Скрипт проверяет статус работы на сервере `dewman.org`. В случае, если работа проверена, отправляет уведомление в
 telegram. Если работ после проверки нет, то скрипт будет продолжать слать запросы на сервер, пока не получит ответ
 о проверке.

 Пример отправленного сообщения в telegram:

 ![Уведомление о проделанной работе](https://github.com/Aleksashka301/work_inspection_notices/blob/main/img/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202025-05-05%20171536.png)

## Для работы скрипта
### GitHub репозиторий
Для запуска необходимо скачать репозиторий
```
git clone https://github.com/Aleksashka301/work_inspection_notices
```
### Виртуальное окружение
Установить виртуальное окружение
```
python -m venv venv
```
Активировать виртуальное окружение
```
venv\Scripts\activate
```
### Зависимости
Установить зависимости
```
pip install -r requirements.txt
```
### Переменные окружения
В корневой папке создать файл `.env` для переменных окружения и добавить туда следующие переменные
1. `DEWMAN_TOKEN` - токен для работы с api dewman
2. `TELEGRAM_TOKEN` - токен телеграм бота. Выдаётся при регистрации бота. Если имеется зарегистрированный бот, то
можно узнать его токен у `@BotFather`
3. `CHAT_ID` - id чата. Можно узнать его в телеграме через `@userinfobot`
### Запуск скрипта
После можно запускать скрипт командой
```python
python main.py
```
