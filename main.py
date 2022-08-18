from flask import Flask, Response, request, redirect, url_for
from math import sqrt, factorial
import sympy
import requests

TOKEN = '5692289016:AAE5u76CPfvDUUtqBFhzVwgGlbVpT-DtUB4'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=https://c2cd-82-80-173-170.ngrok.io/message'.format(TOKEN)

requests.get(TELEGRAM_INIT_WEBHOOK_URL)

app = Flask(__name__)


def prime(message_list: list[str]) -> str:
    is_prime_res = False
    if len(message_list) == 1:
        if message_list[0].isdigit():
            num = int(message_list[0])
            if num == 2 or num % 2:
                is_prime_res = sympy.isprime(num)
            else:
                return "Come on dude, you know even numbers are not prime"

    return "The number is prime!" if is_prime_res else "The number isn't prime"


def is_factorial(message_list: list[str]) -> str:
    is_factorial_res = False
    if len(message_list) == 1 and message_list[0].isdigit():
        num = int(message_list[0])

        if num == 0:
            is_factorial_res = True

        for i in range(num + 1):
            factorial_res = factorial(i)
            if factorial_res == num:
                is_factorial_res = True
                break
            elif factorial_res > num:
                is_factorial_res = False
                break

    return "Factorial" if is_factorial_res else "Not factorial!"


def palindrome(message_list: list[str]) -> str:
    is_palindrome_res = False
    if len(message_list) == 1:
        is_palindrome_res = message_list[0].isdigit() and message_list[0] == message_list[0][::-1]
    return "Palindrome" if is_palindrome_res else "Not palindrome!"


def sqrt_check(message_list: list[str]) -> str:
    is_has_int_sqrt = False
    if len(message_list) == 1:
        if message_list[0].isdigit():
            num = int(message_list[0])
            is_has_int_sqrt = num > 0 and sqrt(num).is_integer()

    return "Has integer square root." if is_has_int_sqrt else "No integer square root."


OPERATIONS = {"/prime": prime, "/palindrome": palindrome, "/sqrt": sqrt_check, "/factorial": is_factorial}


@app.route('/message', methods=["POST"])
def handle_message():
    print("here")
    print(request.get_json())
    first_key = get_first_key()
    if first_key:
        chat_id = request.get_json()[first_key]['chat']['id'] if first_key else None
        user_input = request.get_json()[first_key]['text']
        user_input_list = user_input.split()
        key = user_input_list[0]
        return_msg = OPERATIONS[key](user_input_list[1:]) if key in OPERATIONS.keys() else "Invalid command."
        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(TOKEN, chat_id, return_msg))
        # return redirect(url_for('handle_prime'))
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
