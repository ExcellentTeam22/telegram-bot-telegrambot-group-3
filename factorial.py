import math


def is_factorial(num):
    if num == 0:
        return True

    for i in range(num + 1):
        factorial = math.factorial(i)
        print(factorial)
        if factorial == num:
            return True
        elif factorial > num:
            return False


print(is_factorial(120))
