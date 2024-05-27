import random

class CLA:
    def __init__(self):
        self.validation_number_set = set()

    def get_validation_numbers(self):
        return self.validation_number_set

    # def __del__(self):
    #     self.validation_number_set.remove(self.validation_number)

    def random_validation_number(self):
        while True:
            number = random.randint(0, 2 ** 32 - 1)

            if len(self.validation_number_set) >= 2 ** 32:
                raise Exception("No more validation numbers available")

            if number not in self.validation_number_set:
                self.validation_number_set.add(number)
                return number
