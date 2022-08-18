from flask import Flask, Response, request
import requests

TOKEN = '5692289016:AAE5u76CPfvDUUtqBFhzVwgGlbVpT-DtUB4'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=https://ea24-82-80-173-170.ngrok.io/message'.format(TOKEN)

requests.get(TELEGRAM_INIT_WEBHOOK_URL)

app = Flask(__name__)


@app.route('/message', methods=["POST"])
def handle_message():
    print("got message")
    chat_id = request.get_json()['message']['chat']['id']
    print(chat_id)
    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                       .format(TOKEN, chat_id, "Got it"))
    return Response("success")


if __name__ == '__main__':
    app.run(port=5002)
