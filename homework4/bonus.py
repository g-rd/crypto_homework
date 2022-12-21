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


PRIMENO = 61
generator = 12


secretVal = randint(1, 97)

X = pow(generator, secretVal) % PRIMENO
y = randint(1, PRIMENO)
Y = pow(generator, y) % PRIMENO

print("Alice (the Prover) generates these values:")
print("secretVal(secret)= ", secretVal)
print("PRIMENO= ", PRIMENO)
print("X= ", X)

print("\nAlice generates a random value (y):")
print("y=", y)

print("\nAlice computes Y = generator^y \
(mod PRIMENO) and passes to Sachin:")

print("Y=", Y)

print("\nSachin generates a random value (c) and\
passes to Alice:")

c = randint(1, 97)
print("c=", c)
print("\nAlice calculates z = y.secretVal^c \
(mod PRIMENO) and send to Sachin (the Verifier):")

z = (y + c * secretVal)

print("z=", z)

print("\nSachin now computes val=generator^z (mod PRIMENO)\
and (Y X^c (mod PRIMENO)) and determines if they are the same\primeNo")

val1 = pow(generator, z) % PRIMENO
val2 = (Y * (X**c)) % PRIMENO

print("val1= ", val1, end=' ')
print(" val2= ", val2)

if (val1 == val2):
	print("Alice has proven that she knows x")
else:
	print("Failure to prove")

alice = Alice()
bob = Bob()
bob.set_y(alice.get_y())


q = prime_number = 61
# Choose generator Z_q
g = generator = randint(1, prime_number - 1)
# choose random a and b in Z_q
a = randint(1, prime_number - 1)
b = randint(1, prime_number - 1)
x = private_x = (a + b) % q
#Schnorr scheme
z = pow(g, x, q)
# This is pub key available to Bob: z
# Alice picks random r = randint(1, q-1) value
r = randint(1, q - 1)
# Alice sends h to Bob
h = pow(g, r, q)
# Bob chooses c = randint(1, q-1)
c = randint(1, q-1)
# Bob sends c to Alice
# Alice computes s = (r + (c * x)) % q
s = (r + (c * x)) % q
# Alice sends s to Bob
# Bob check if h * (z**c) % q == g**s % q
assert h * (z**c) % q == g**s % q