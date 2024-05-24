import time
import math

class ReduceLinear:
    def __init__(self, quantity=None):
        self.init_logical()
        self.list_ri = []
        if quantity is not None:
            self.generate_numbers_ri(quantity)

    def init_logical(self):
        self.seed = int(time.time() * 1000)  # current time in milliseconds
        self.a = 1664525
        self.c = 7
        self.m = int(math.pow(2, 32))

    def generate_numbers_ri(self, quantity):
        for _ in range(quantity):
            random_number = self.generate_ri()
            if random_number > 1:
                print(f"Error: ri is greater than 1. ri = {random_number}")
            self.list_ri.append(random_number)

    def generate_ri(self):
        self.seed = ((self.a * self.seed) + self.c) % self.m
        return self.seed / self.m

    def get_next_ri(self):
        if self.list_ri:
            return self.list_ri.pop(0)
        else:
            return None
