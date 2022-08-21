from flask import Flask, Response, request, redirect, url_for
import requests

TOKEN = '5559141211:AAGsg_iBhfZd-Wr_lW8bZN0kqREdPKP4g5w'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=https://eb66-82-80-173-170.ngrok.io/message'.format(TOKEN)

requests.get(TELEGRAM_INIT_WEBHOOK_URL)

app = Flask(__name__)


@app.route('/message', methods=["POST"])
def handle_message():
    first_key = get_first_key()
    if first_key:
        chat_id = request.get_json()[first_key]['chat']['id']
        user_input = request.get_json()[first_key]['text']
        # user_input_list = user_input.split()
        # validation
        # key = user_input_list[0]
        # return_msg = OPERATIONS[key](user_input_list[1:]) if key in OPERATIONS.keys() else "Invalid command."
        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(TOKEN, chat_id, 'Got massage'))
    return Response("success")


def get_first_key() -> str:
    first_key = None
    if 'message' in request.get_json().keys():
        first_key = 'message'
    if 'edited_message' in request.get_json():
        first_key = 'edited_message'
    return first_key


if __name__ == '__main__':
    app.run(port=5002)
