from random import randint


class Bob:

    def __init__(self, verbose=False):
        self.h_1 = None
        self.h_2 = None
        self.y_1 = None
        self.y_2 = None
        self.verbose = verbose

    def listen(self, hashes):
        h_1, h_2 = hashes
        if self.verbose:
            print(f"Bob got hashes: {h_1, h_2}")
        self.h_1 = h_1
        self.h_2 = h_2

    def send_c(self):
        return randint(1, 10)

    def get_y_values(self, y_values):
        if self.verbose:
            print(f"Bob got y values: {y_values}")
        y_1, y_2 = y_values
        self.h_1 = y_1
        self.y_2 = y_2

    def verify(self):
        verified = False
        if self.y_1 and self.y_2:
            if self.y_1 * self.y_2 == self.h_1 * self.h_2:
                verified = True
        return verified


class Alice:
    def __init__(self, verbose=False):
        self.c = None
        self.g = randint(1, 10)
        self.a = randint(1, 10)
        self.b = randint(1, 10)
        self.x = self.a + self.b
        self.r_1, self.r_2 = randint(1, 10), randint(1, 10)
        self.verbose = verbose

    def send_hashes(self):
        return self.g**self.r_1, self.g**self.r_2

    def get_c(self, c_value):
        if self.verbose:
            print(f"Alice got c value: {c_value}")
        self.c = c_value

    def send_y_values(self):
        if self.c:
            return self.c + self.a, self.c + self.b


alice = Alice(verbose=True)
bob = Bob(verbose=True)
print(f"First alice sends hashes to Bob {alice.send_hashes()}")
bob.listen(alice.send_hashes())
print(f"Bob generate c and sends to Alice {bob.send_c()}")
alice.get_c(bob.send_c())
print(f"Alice sends bob y values: {alice.send_y_values()}")
bob.get_y_values(alice.send_y_values())
print(f"Bob verifies the communication: {bob.verify()}")

count_of_verified = 0
for i in range(0, 100):
    alice = Alice()
    bob = Bob()
    bob.listen(alice.send_hashes())
    alice.get_c(bob.send_c())
    bob.get_y_values(alice.send_y_values())
    if bob.verify():
        count_of_verified += 1
        print(f"Verified times: {count_of_verified}")
print(f"Bob has verified Alice {count_of_verified} times")

