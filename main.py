import logging
import requests
import telegram

from environs import Env


class TelegramLogsHandler(logging.Handler):
    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def send_notice(response, bot, chat_id):
    lesson_notice = response['new_attempts'][0]
    lesson = lesson_notice['lesson_title']
    lesson_link = lesson_notice['lesson_url']

    if lesson_notice['is_negative']:
        work_status = 'К сожалению в работе нашлись ошибки.'
    else:
        work_status = 'Преподавателю всё понравилось, можно приступать к следующему уроку.'

    bot.send_message(chat_id=chat_id, text=f'У вас проверили работу "{lesson}". {work_status} {lesson_link}')


if __name__ == '__main__':
    env = Env()
    env.read_env()

    dewman_token = env.str('DEWMAN_TOKEN')
    telegram_token = env.str('TELEGRAM_TOKEN')
    chat_id = env.int('CHAT_ID')

    dewman_url = 'https://dvmn.org/api/long_polling/'
    header = {'Authorization': dewman_token,}
    bot = telegram.Bot(token=telegram_token)

    tg_handler = TelegramLogsHandler(bot, chat_id)
    tg_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
    tg_handler.setFormatter(formatter)

    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(levelname)s - %(message)s')
    logging.getLogger().addHandler(tg_handler)
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.info('Бот запущен')

    while True:
        try:
            try:
                response = requests.get(dewman_url, headers=header, timeout=60)
                response.raise_for_status()
                response = response.json()
            except requests.exceptions.ReadTimeout:
                continue
            except Exception as error:
                logging.exception(error)
                logging.critical('Работа бота прекращена!')
                break

            try:
                header['timestamp'] = str(response['timestamp_to_request'])
            except KeyError:
                header['timestamp'] = str(response['last_attempt_timestamp'])

            if response['status'] == 'found':
                send_notice(response, bot, chat_id)
        except Exception as error:
            logging.exception(error)
            continue
