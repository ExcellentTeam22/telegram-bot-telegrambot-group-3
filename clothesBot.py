from flask import Flask, Response, request, redirect, url_for
import requests

TOKEN = '5559141211:AAGsg_iBhfZd-Wr_lW8bZN0kqREdPKP4g5w'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=https://c2cd-82-80-173-170.ngrok.io/message'.format(TOKEN)

API_KEY = "0ecef89c9794b99021d3c035ab117555"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

requests.get(TELEGRAM_INIT_WEBHOOK_URL)

app = Flask(__name__)


def get_weather(city_name):
    complete_url = BASE_URL + "appid=" + API_KEY + "&q=" + city_name + "&units=metric"

    response = requests.get(complete_url)
    weather = response.json()

    if weather["cod"] != "404":
        current_temperature = weather["main"]["temp"]
        status = weather["weather"][0]["main"]
        return status == "Rain", int(current_temperature)

    else:
        return None  # if the city was not found


OPERATIONS = {"/city": get_weather}


@app.route('/message', methods=["POST"])
def handle_message():
    first_key = get_first_key()
    if first_key:
        chat_id = request.get_json()[first_key]['chat']['id'] if first_key else None
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
