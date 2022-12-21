from math import gcd
from random import randint


class Alice:
    def __init__(self, verbose=False):
        self.c = None
        self.g = q = 61
        self.a = randint(1, self.g-1)
        self.b = 7
        self.x = self.a + self.b
        self.verbose = verbose

    def get_g(self):
        return self.g

    def get_hashes(self):
        """
        We removed the hashes, because they don't help.
        :return:
        """
        return None

    def set_c(self, c_value):
        """
        Bob send a c value to Alice to have some input for Alice to prove herself.
        :param c_value:
        :return:
        """
        if self.verbose:
            print(f"Alice got c value: {c_value}")
        self.c = c_value

    def get_y(self):
        """
        Alice signs the message y.
        :return:
        """
        return self.x**2 % self.g


class Bob:

    def __init__(self, verbose=False):
        self.g = None
        self.x = None
        self.y = None
        self.c = None
        self.verbose = verbose

    def set_g(self, g):
        self.g = g

    def listen(self, hashes):
        """
        There is no need for this anymore.
        :param hashes:
        :return:
        """
        return None

    def get_c(self):
        self.c = randint(1, 10)
        return self.c

    def set_y(self, y_value):
        self.y = y_value
        print(self.y)

    def verify(self):
        pass


q = prime_nr = 7
# Choose generator Z_q
g = generator = randint(1, prime_nr - 1)
# choose random a and b in Z_q
a = randint(1, prime_nr - 1)
b = randint(1, prime_nr - 1)
z = (a + b) % prime_nr
x = pow(generator, z, prime_nr) # This is pub key available to Bob

#Schnorr scheme
# Alice picks random r = randint(1, q-1) value
r = randint(1, q - 1)
# Alice sends h to Bob
h = pow(generator, r, prime_nr)
# Bob chooses c = randint(1, q-1)
c = randint(1, q-1)
# Bob sends c to Alice
# Alice computes s = (r + (c * x)) % q
#s = (r + (c * x)) % q
y = (r + (c * z))
# Alice sends s to Bob
# Bob check if h * (z**c) % q == g**s % q
assert h * (x ** c) % q == g ** y % q