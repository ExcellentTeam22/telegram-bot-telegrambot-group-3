import consts

class SingletonMeta(type):
    """From https://refactoring.guru/design-patterns/singleton/python/example, singleton meta class"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class FindOutfit(metaclass=SingletonMeta):
    def __int__(self):
        self.__temperature_dict = {}
        self.__outfit_dict = {}
        self.__lowest_key = -50
        self.__highest_key = 50
        self.__create_temperature_dict()
        self.__create_outfit_dict()

    def __create_temperature_dict(self):
        for num in range(self.__lowest_key, self.__highest_key + 1):
            if num < 2:
                self.__temperature_dict[num] = "Very cold"
            elif num <= 13:
                self.__temperature_dict[num] = "Cold"
            elif num <= 22:
                self.__temperature_dict[num] = "Sunny"
            else:
                self.__temperature_dict[num] = "Hot"

    def __create_outfit_dict(self):
        self.__outfit_dict[("Very cold", consts.MALE)] = "You should wear several layers, put on a long shirt," \
                                                         " coat and long pants, thick socks, and closed shoes." \
                                                         "You should also add a scarf."
        self.__outfit_dict[("Very cold", consts.FEMALE)] = "You should wear several layers, put on a long shirt," \
                                                           " sweater, and long pants. You should also add a scarf," \
                                                           " and gloves and wear boots."
        self.__outfit_dict[("Cold", consts.MALE)] = "You should wear a few layers that include a thick jacket and a " \
                                                    "short shirt. You should wear long pants and closed shoes."
        self.__outfit_dict[("Cold", consts.FEMALE)] = "You should wear a few layers that include a long shirt," \
                                                      " sweater, and closed shoes."
        self.__outfit_dict[("Sunny", consts.MALE)] = "You should wear a thin long shirt, long pants, and closed shoes" \
                                                     " but they could be open too."
        self.__outfit_dict[("Sunny", consts.FEMALE)] = "You should wear a thin long shirt, long pants, and closed " \
                                                       "shoes.Option: Jacket ."
        self.__outfit_dict[("Hot", consts.MALE)] = "You should wear shorts, a short shirt, and flip-flops."
        self.__outfit_dict[("Hot", consts.FEMALE)] = "You should wear shorts, a short shirt, or a dress, maybe a " \
                                                     "skirt, and open shoes."

    """, user: User"""
    def get_best_outfit_message(self, lowest_temperature: int, highest_temperature: int,
                                is_rainy: bool = False) -> str:
        lowest_temperature_in_dict = max(lowest_temperature + user.bonuse, self.__lowest_key)
        highest_temperature_in_dict = min(highest_temperature + user.bonuse, self.__highest_key)
        night_outfit = self.__outfit_dict[(self.__temperature_dict[lowest_temperature_in_dict], user.gender)]
        day_outfit = self.__outfit_dict[(self.__temperature_dict[highest_temperature_in_dict], user.gender)]
        return_message = "Recommendation" + (" for day: " + day_outfit + "\nRecommendation for night: " + night_outfit)\
            if night_outfit != day_outfit else (": " + day_outfit)
        if is_rainy:
            return_message += "\nDon't forget to take a raincoat and an umbrella. It's going to be rainy outside."
        return return_message


if __name__ == "__main__":
    pass