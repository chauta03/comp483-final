import random

validation_number_set = set()

def random_validation_number():
    while True:
        number = random.randint(0, 2 ** 32 - 1)
        if number not in validation_number_set:
            validation_number_set.add(number)
            return number
    return 