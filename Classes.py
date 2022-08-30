import consts


class User:
    def __init__(self):
        self.counter = 0
        self.degrees_bonus = 0
        self.name = ""
        self.gender = ""
        self.is_suffer = None

    # getter methods
    def get_name(self):
        return self.name

    def get_gender(self):
        return self.gender

    def get_degrees_bonus(self):
        return self.degrees_bonus

    def get_counter(self):
        return self.counter

    # setter methods
    def set_username(self, user_input: list[str]):
        self.name = "".join(user_input)
        if self.name == "":
            raise ValueError("Invalid name, enter your name.")
        if self.counter < consts.ATTRIBUTE_NUMBER:
            self.counter += 1

    def set_gender(self, user_input: list[str]):
        if len(user_input) != 1 or (user_input[0].lower() != "male" and user_input[0].lower() != "female"):
            raise ValueError("Invalid gender, enter male or female.")
        self.gender = consts.MALE if user_input[0].lower() == "male" else consts.FEMALE
        if self.counter < consts.ATTRIBUTE_NUMBER:
            self.counter += 1

    def set_is_suffer(self, user_input: list[str]):
        if len(user_input) != 1 or (user_input[0].lower() != "y" and user_input[0].lower() != "n"):
            raise ValueError("Invalid input, enter 'Y' for yes or 'N' for No.")
        self.is_suffer = True if user_input[0].lower() == "y" else False
        if self.counter < consts.ATTRIBUTE_NUMBER:
            self.counter += 1

    # other methods
    def calculate_bonus(self):
        self.degrees_bonus = -2 if self.gender == consts.FEMALE else 0
        self.degrees_bonus += 3 if self.is_suffer else 0
