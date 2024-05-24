import random

validation_number_set = set()

def random_validation_number():
    while True:
        number = random.randint(0, 2 ** 32 - 1)

        if len(random_validation_number) >= 2 ** 32:
            raise Exception("No more validation numbers available")

        if number not in validation_number_set:
            validation_number_set.add(number)
            return number

def get_validation_number_set():
    return validation_number_set