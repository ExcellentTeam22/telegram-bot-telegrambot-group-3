from flask import Flask, Response, request, redirect, url_for
import requests
import Classes
import clothes_data_structure as clothes
import consts

user_dic = {}

requests.get(consts.TELEGRAM_INIT_WEBHOOK_URL)

app = Flask(__name__)


def set_name(chat_id: str, name: list[str]):
    user_dic[chat_id].set_username(name)


def set_gender(chat_id: str, gender: list[str]):
    user_dic[chat_id].set_gender(gender)


def set_suffer(chat_id: str, suffer: list[str]):
    user_dic[chat_id].set_is_suffer(suffer)


def initial_registration(first_key: str, chat_id: str):
    if chat_id not in user_dic.keys():
        user = Classes.User()
        user_dic[chat_id] = user

    if user_dic[chat_id].get_name() == "":
        requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(consts.TOKEN, chat_id,
                                                                                    'What is your name? (/name ...)'))
    elif user_dic[chat_id].get_gender() == "":
        requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(consts.TOKEN, chat_id,
                                                            'What is your gender? (/gender Male or /gender Female)'))

    elif user_dic[chat_id].get_is_suffer() == "":
        requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(consts.TOKEN, chat_id,
                                                            'Do you suffer when it\'s hot outside? (/suffer Y or N)'))


def get_weather(city_name: list[str]):
    city_name = "".join(city_name)
    complete_url = consts.BASE_URL + "appid=" + consts.API_KEY + "&q=" + city_name + "&units=metric"
    response = requests.get(complete_url)
    weather = response.json()

    if weather["cod"] != "404":
        current_temperature = weather["main"]["temp"]
        status = weather["weather"][0]["main"]
        return status == "Rain", int(current_temperature)
    else:
        return None  # if the city was not found


OPERATIONS = {"/name": set_name, "/gender": set_gender, "/sufffer": set_suffer}


@app.route('/message', methods=["POST"])
def handle_message():
    first_key = get_first_key()
    if first_key:
        chat_id = request.get_json()[first_key]['chat']['id']
        user_input = request.get_json()[first_key]['text']
        user_input_list = user_input.split()
        key = user_input_list[0]
        try:
            return_msg = OPERATIONS[key](chat_id, user_input_list[1:]) if key in OPERATIONS.keys() else "Invalid command."
        except ValueError as error:
            requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(consts.TOKEN, chat_id, error))

        if chat_id not in user_dic.keys() or user_dic[chat_id].get_counter() < consts.ATTRIBUTE_NUMBER:
            initial_registration(first_key, chat_id)

        else:
            user_dic[chat_id].calculate_bonus()

            if user_input_list[0] == '/city':
                is_rain, temp = get_weather(user_input_list[1:])
                requests.get(
                    "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(consts.TOKEN, chat_id,
                                                           clothes.FindOutfit().get_best_outfit_message(is_rain, temp)))

            else:
                requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(consts.TOKEN, chat_id,
                                        "Hello {}, please enter city (/city ...)".format(user_dic[chat_id].get_name())))

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
