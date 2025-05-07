from environs import Env
import requests
import telegram


def sending_message(response, bot, chat_id):
    lesson_notice = response['new_attempts'][0]
    lesson = lesson_notice['lesson_title']
    lesson_link = lesson_notice['lesson_url']

    if lesson_notice['is_negative']:
        work_status = 'К сожалению в работе нашлись ошибки.'
    else:
        work_status = 'Преподавателю всё понравилось, можно приступать к следующему уроку.'

    bot.send_message(chat_id=chat_id, text=f'У вас проверили работу "{lesson}". {work_status} {lesson_link}')


if __name__ in '__main__':
    env = Env()
    env.read_env()

    dewman_token = env.str('DEWMAN_TOKEN')
    telegram_token = env.str('TELEGRAM_TOKEN')
    chat_id = env.int('CHAT_ID')

    dewman_url = 'https://dvmn.org/api/long_polling/'
    header = {'Authorization': dewman_token,}
    bot = telegram.Bot(token=telegram_token)

    while True:
        try:
            response = requests.get(dewman_url, headers=header, timeout=60)
            response.raise_for_status()
            response = response.json()
        except requests.exceptions.ReadTimeout:
            continue

        try:
            header['timestamp'] = str(response['timestamp_to_request'])
        except KeyError:
            header['timestamp'] = str(response['last_attempt_timestamp'])

        if response['status'] == 'found':
            break

    sending_message(response, bot, chat_id)
