from math import ceil, sqrt, gcd
from random import randint
from typing import Tuple


def extended_eucleidian(a, b):
    """
    Used to calculate modular inverse.
    :param a:
    :param b:
    :return:
    """
    results = list()

    # To begin we know that s1 = 1, s2 = 0 and t1 = 0 and t2 = 1
    s1 = 1
    t1 = 0
    s2 = 0
    t2 = 1

    def recursive(left, remainder):
        nonlocal s2
        nonlocal s1
        nonlocal t1
        nonlocal t2

        # Python way to divide without remainder
        q = left // remainder
        # Coefficient s_i+2 = s_i - q*s_i+1
        si = s1 - q * s2
        s1 = s2
        s2 = si

        # Coefficient t_i+2 = ti - q*ti_+1
        ti = t1 - q * t2
        t1 = t2
        t2 = ti

        new_remainder = left % remainder
        left = q * remainder + new_remainder

        results.append([left, q, remainder, new_remainder, s2, t2])
        if new_remainder != 0:
            recursive(remainder, new_remainder)

    recursive(a, b)
    return results


def modular_inverse(a, mod):
    """
    Calculate the modular inverse of a in modulo mod.
    :param a: integer to inverse.
    :param mod: modulo
    :return: return the inverse of a.
    """
    _gcd = extended_eucleidian(mod, a)
    if not _gcd[-1][2] == 1:
        # there exists an inverse only if the numbers are relatively prime.
        print("There is no inverse")
        return None
    else:
        if _gcd[-2][-1] < 0:
            # return a positive inverse.
            return mod + _gcd[-2][-1]
        return _gcd[-2][-1]


def baby_step_giant_step(base: int, result: int, prime: int) -> int:
    """
    Solve for x in g^x ≡ h (mod p) given integers g, h, and p.

    If p is not prime, you shouldn't use BSGS.
    """
    # Calculate m as the ceiling of the square root of p
    m = ceil(sqrt(prime))

    # Precompute g^i (mod p) for i in [0, m]
    baby_steps = {}
    for j in range(m):
        b = pow(base, j, prime)
        baby_steps[j] = b

    # Precompute g^(im) (mod p) for i in [1, m]
    giant_step = pow(base, m * (prime - 2), prime)

    # Search for an equivalence in the baby_steps table
    giant_steps = {}
    for i in range(m):
        y = (result * pow(giant_step, i, prime)) % prime
        giant_steps[i] = y

    solution = None
    for g_key, g_value in giant_steps.items():
        for b_key, b_value in baby_steps.items():
            if g_value == b_value:
                solution = g_key * m + b_key

    if not solution:
        raise ValueError("No Solution Found for the input given.")
    else:
        return solution


def generate_private_key(p):
    """
    The function first generates a private key x using the generate_private_key function,
    which chooses a random integer between 0 and p-1 such that the greatest common divisor
    (GCD) of p-1 and x is 1.
    This ensures that x is relatively prime to p-1,
    which is a necessary condition for the ElGamal cryptosystem to work.

    :param p: prime_number
    :return: private_key
    """
    key = randint(0, p - 1)
    while gcd(p - 1, key) != 1:
        key = randint(0, p - 1)
    return key


def generate_keys(prime_number: int, generator: int, who) -> Tuple[int, int]:
    """
    Generate the public and private key.
    :param prime_number: a chosen prime_number
    :param generator: a chosen generator
    :param who: Who is generating keys (Used for nice printouts).
    :return: public_key, private_key
    """
    # Generate a private key
    print(f"{str(who).capitalize()} calculates her keys.")
    print(f"{str(who).capitalize()} calculates her private key such that it is:")
    print(f" 1 < key < p - 1 and gcd(key, p-1) == 1")
    private_key = generate_private_key(prime_number)

    # Calculate the public key as generator^private_key mod prime_number
    public_key = pow(generator, private_key, prime_number)
    print(f"{who} calculates her public key:"
          f" y = g^x mod p = {generator}^{private_key} mod {prime_number} = {public_key}")
    print("\n")
    return private_key, public_key


class Elgamal:
    """
    NB!: This Elgamal is not secure. It is written only to demonstrate the chosen ciphertext attack.
    """
    def __init__(self, priv_key, pub_key, prime_number, generator):
        self.priv_key = priv_key
        self.pub_key = pub_key
        self.prime_number = prime_number
        self.generator = generator

    def encrypt(self, message: int) -> Tuple[int, int]:
        """
        Elgamal encryption method.
        :param message: Message to encrypt
        :param prime_number: Prime number used for the modulos
        :param generator: The generator
        :param public_key: Public key
        :return: ciphertext in the form of a tuple of (c1, c2)
        """

        c1 = pow(self.generator, self.priv_key, self.prime_number)
        print(f"C1 = g^k mod p = {self.generator}^{self.priv_key} mod {self.prime_number} = {c1}")

        s = pow(self.pub_key, self.priv_key, self.prime_number)  # The shared secret
        c2 = (message * s) % self.prime_number

        print(f"C2 = m * s mod p = {message} * {s} mod {self.prime_number} = {c2}")

        return c1, c2

    def decrypt(self, c1: int, c2: int) -> int:
        """
        Elgamal decryption method.
        :param c1: cipher part1
        :param c2: cipher part2
        :return:
        """
        # Calculate the modular inverse of c1^private_key modulo prime_number
        c_prime = pow(c1, self.priv_key, self.prime_number)
        c_prime_inv = modular_inverse(c_prime, self.prime_number)

        # Calculate the decryption of the ciphertext as the original message m
        m = (c2 * c_prime_inv) % self.prime_number

        return m


def task_one():
    print("------------")
    print("TASK 1.1")
    print("------------")
    alice_prime = 19777
    alice_generator = 51
    alice_priv, alice_pub = generate_keys(alice_prime, alice_generator, "Alice")
    Alice = Elgamal(
        priv_key=alice_priv,
        pub_key=alice_pub,
        prime_number=alice_prime,
        generator=alice_generator
    )
    alice_message = 115
    alice_c1, alice_c2 = Alice.encrypt(alice_message)
    alice_decrypted = Alice.decrypt(alice_c1, alice_c2)
    print(f"Alice decrypted: {alice_decrypted} and the orig message was: {alice_message}\n")
    print(f"Eve intercepts: {alice_c1, alice_c2}")

    print(f"Eve uses Alices public key, generator and prime to calculate her own keys.")
    eve_priv, eve_pub = generate_keys(alice_prime, alice_generator, "Eve")

    Eve = Elgamal(
        priv_key=eve_priv,
        pub_key=alice_pub,
        prime_number=alice_prime,
        generator=alice_generator
    )

    eve_message = 16
    print(f"Eve chooses another message that she either encrypts herself or asks a friend to encrypt: {eve_message}")
    eve_c1, eve_c2 = Eve.encrypt(eve_message)
    print(f"She now has a new ciphertext c' = ({eve_c1}, {eve_c2})")
    print(f"Eve uses the homomorphic property of Elgamal to construct a new ciphertext based on her own \n"
          f"ciphertext and the one she intercepted by multiplying them together.")
    new_c1, new_c2 = ((alice_c1 * eve_c1) % alice_prime, (alice_c2 * eve_c2) % alice_prime)
    print(f"The new ciphertext is {new_c1, new_c2}")
    print(f"she will ask her friend to decrypt the new ciphertext that she constructed.")

    Friend = Alice

    friend_decrypts = Friend.decrypt(new_c1, new_c2)
    print(f"Her friend will give her the new decrypted message: {friend_decrypts}\n")
    print(f"Eve will have to use multiplicative inverse on her own message in order to decrypt the original message.\n"
          f"This is done to remove her own message from the product that she created earlier, \n"
          f"by multiplying the inverse of her message with the original message.")
    inverse_eve_m = modular_inverse(eve_message, alice_prime)

    print(f"inverse_of_eves_message * decrypted_fiends_message mod prime_number")
    print(f"{inverse_eve_m} * {friend_decrypts} mod {alice_prime}")
    original_message_decrypted = (inverse_eve_m * friend_decrypts) % alice_prime
    print(f"Eve has successfully deciphered the original message: {original_message_decrypted}")
    print(f"Original message decrypted with the private key: {alice_decrypted}")
    print(f"This works because Elgamal is homomorphic.")
    print("------------")


def task_two():
    print("TASK 1.2")
    print("------------")
    """
    If adversary Carol intercepts two messages c1 = (c11, c12) and c2 = (c21, c22) and she notices that c11 = c21.
    Adversary carol knows that the first part of Elgamal cipher is calculated by:
    c11 = generate^private_key mod prime_number and c21 = generate^private_key mod prime_number.

    From this Carol can conclude that g^pk1 is equal to g^k2 mod p. Carol also knows that the messages has no impact on the
    first part of the Elgamal cipher and that for each message the modulus and generator are the same.

    From this we can conclude that the private_key must have been the same for both messages to end up with the
    situation where c11 = c21. 

    This also means that the private_key has to be the same for c2 when c2 was calculated using c2 = m * (y^k mod p) mod p 

    """
    m1 = 411
    m2 = 63
    alice_prime = 19777
    alice_generator = 51
    alice_priv, alice_pub = generate_keys(alice_prime, alice_generator, "Alice")
    Alice = Elgamal(
        priv_key=alice_priv,
        pub_key=alice_pub,
        prime_number=alice_prime,
        generator=alice_generator
    )

    print(f"Suppose we have two messages '{m1}' and '{m2}'")
    print(f"And we know that the prime_number, generator and pub_key are known (they are public).")

    print(f"prime: {alice_prime}, generator: {alice_generator}, public_key: {alice_pub}")

    c11, c12 = (pow(alice_generator, alice_priv, alice_prime), (m1 * pow(alice_pub, alice_priv, alice_prime)))
    c21, c22 = (pow(alice_generator, alice_priv, alice_prime), (m2 * pow(alice_pub, alice_priv, alice_prime)))

    print(f"Suppose Carol intercepted two messages such that: {c11, c12} and {c21, c22}")
    m = Alice.decrypt(c11, c12)
    print(f"Demonstrate that Alice can decrypt m1 using {c11, c12}: {m} ")
    print(f"Carol notices that: c12 = c22")
    print(f"Carol knowing how Elgamal works concludes that the private key used to encrypt the messages must be the same.")

    print(f"Carol could try to use baby-step giant-step algorithm to find the private_key")
    private_key = baby_step_giant_step(alice_generator, c11, alice_prime)

    print(f"k: {private_key} = alice_priv: {alice_priv}")

    print(f"Since the second part is calculated as message * public_key^{private_key} mod {alice_prime}")
    c1_break = pow(alice_pub, private_key, alice_prime)
    c2_break = pow(alice_pub, private_key, alice_prime)
    inv_c1_break = modular_inverse(c1_break, alice_prime)
    inv_c2_break = modular_inverse(c2_break, alice_prime)
    broken_c1_message = (c12 * inv_c1_break % alice_prime)
    broken_c2_message = (c22 * inv_c2_break % alice_prime)
    print(f"This way we can actually find the values m1: {broken_c1_message} and m2: {broken_c2_message}")
    print(
        f"Other than that she can only find that: \n"
        f"m1/m2 = (m1 * alice_pub^alice_priv mod alice_prime) / (m1 * alice_pub^alice_priv mod alice_prime) = c12/c22 \n"
        f"and nothing else interesting. This only shows that the product of \n"
        f"messages is related to the product of ciphers."
    )
    print(f"Example: c12 / c22: = {c12 / c22}")
    print(f"(m1 * alice_pub^alice_priv mod alice_prime) / (m2 * alice_pub^alice_priv mod alice_prime) = "
          f"{(m1 * pow(alice_pub, alice_priv, alice_prime)) / (m2 * pow(alice_pub, alice_priv, alice_prime))}")
    print(f"m1 / m2: {m1 / m2}")
    print("------------")


task_one()
task_two()
