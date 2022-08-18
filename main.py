from flask import Flask, Response, request
from math import sqrt
import requests

TOKEN = '5692289016:AAE5u76CPfvDUUtqBFhzVwgGlbVpT-DtUB4'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=https://b673-82-80-173-170.ngrok.io/message'.format(TOKEN)

requests.get(TELEGRAM_INIT_WEBHOOK_URL)

app = Flask(__name__)


def is_prime(num: int) -> bool:
    if num > 1:
        # check for factors
        for i in range(2, int(sqrt(num))+ 1):
            if (num % i) == 0:
                return False
        return True
    return False


@app.route('/message', methods=["POST"])
def handle_message():
    chat_id = request.get_json()['message']['chat']['id']
    user_input = request.get_json()['message']['text']
    print(chat_id)
    print(user_input)

    user_input_list = user_input.split()
    is_prime_res = False
    if len(user_input_list) == 1:
        if user_input_list[0].isdigit():
            is_prime_res = is_prime(int(user_input_list[0]))

    return_msg = "Is prime!" if is_prime_res else "Not prime"
    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                       .format(TOKEN, chat_id, return_msg))
    return Response("success")


if __name__ == '__main__':
    app.run(port=5002)
