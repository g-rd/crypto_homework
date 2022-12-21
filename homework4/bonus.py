from math import gcd
from random import randint


class Alice:
    def __init__(self, verbose=False):
        self.q =  7 # prime_nr
        # Choose generator Z_q
        self.g = randint(1, self.q - 1) # generator
        # choose random a and b in Z_q
        self.a = randint(1, self.q - 1)
        self.b = randint(1, self.q - 1)
        self.z = (self.a + self.b) % self.q
        self.x = pow(self.g, self.z, self.q)  # This is pub key available to Bob

        self.c = None
        self.r = None
        self.verbose = verbose

    def get_pub_values(self):
        return self.g, self.x, self.q

    def get_hashes(self):
        """
        We removed the hashes, because they don't help.
        :return:
        """
        r = randint(1, q - 1)
        self.r = r
        h = pow(self.g, r, self.q)
        return h

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
        y = (self.r + (self.c * self.z))
        return y


class Bob:

    def __init__(self, verbose=False):
        self.q = None
        # Choose generator Z_q
        self.g = None
        self.g = None
        self.x = None
        self.h = None
        self.c = None
        self.y = None
        self.c = randint(1, 10)
        self.verbose = verbose

    def set_pub_values(self, g, x, q):
        """
        g: generator
        z: public key
        q: prime_nr
        :param g:
        :param z:
        :param q:
        :return:
        """
        self.g = g
        self.x = x
        self.q = q

    def set_hash(self, h):
        self.h = h

    def get_c(self):
        """
        Bob sends c
        :return:
        """
        return self.c

    def set_y(self, y):
        self.y = y

    def verify(self):

        if self.h * (self.x ** self.c) % self.q == self.g ** self.y % self.q:
            print("Alice, has been verified.")
            pass

# Init Alice
alice = Alice()

# Init Bob
bob = Bob()

# Bob gets public values
g, z, q = alice.get_pub_values()

# Bob sets public values
bob.set_pub_values(g, z, q)

# Alice sends h value to Bob
bob.set_hash(alice.get_hashes())

# Bob sends c value to Alice
alice.set_c(bob.get_c())

# Alice Sends y value to Bob
bob.set_y(alice.get_y())

# Bob verifies Alice
bob.verify()
