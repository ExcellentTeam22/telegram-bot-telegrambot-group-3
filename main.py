from flask import Flask, request, Response
import requests

TOKEN = '5692289016:AAE5u76CPfvDUUtqBFhzVwgGlbVpT-DtUB4'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=http://9baa-2a02-6680-1109-2107-6d9d-bfe8-7df4-58ab.ngrok.io/message'.format(TOKEN)

requests.get(TELEGRAM_INIT_WEBHOOK_URL)

app = Flask(__name__)


@app.route('/')
def sanity():
    return "Server is running"


if __name__ == '__main__':
    app.run(port=5002)
