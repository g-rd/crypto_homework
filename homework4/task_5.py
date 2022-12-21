from random import randint


class Bob:

    def __init__(self, verbose=False):
        self.g = None
        self.x = None
        self.h_1 = None
        self.h_2 = None
        self.y_1 = None
        self.y_2 = None
        self.c = None
        self.verbose = verbose

    def set_g_value(self, g):
        self.g = g

    def listen(self, hashes):
        h_1, h_2 = hashes
        if self.verbose:
            print(f"Bob got hashes: {h_1, h_2}")
        self.h_1 = h_1
        self.h_2 = h_2

    def send_c(self):
        self.c = randint(1, 10)
        return self.c

    def get_y_values(self, y_values):
        if self.verbose:
            print(f"Bob got y values: {y_values}")
        y_1, y_2 = y_values
        self.y_1 = y_1
        self.y_2 = y_2

    def verify(self):
        verified = False
        if self.verbose:
            print(f"Bob verifies with: "
                  f"{self.y_1} * {self.y_2} = {self.h_1} * {self.h_2}")
        if self.y_1 and self.y_2:
            if self.y_1 * self.y_2 == self.h_1 * self.h_2:
                verified = True
        return verified


class Alice:
    def __init__(self, verbose=False):
        self.c = None
        self.g = 17
        self.a = 5
        self.b = 7
        self.x = self.a + self.b
        self.r_1, self.r_2 = randint(1, 10), randint(1, 10)
        self.verbose = verbose

    def get_g_value(self):
        return self.g

    def send_hashes(self):
        return self.g ** self.r_1, self.g ** self.r_2

    def get_c(self, c_value):
        if self.verbose:
            print(f"Alice got c value: {c_value}")
        self.c = c_value

    def send_y_values(self):
        if self.c:
            return self.c + self.a, self.c + self.b


class Eve(Alice):
    def send_hashes(self):
        return 1, 1

    def send_y_values(self):
        return 1, 1


class Evan(Bob):
    def find_the_secrets(self):
        if self.c and self.y_1 and self.y_2:
            a = self.y_1 - self.c
            b = self.y_2 - self.c
            if self.verbose:
                print(f"Evan found out a: {a} and b: {b}")
            return a, b


def completeness():
    ## Legitimate communication.

    alice = Alice(verbose=True)
    bob = Bob(verbose=True)
    bob.g = alice.g
    bob.x = alice.x
    print(f"Bob knows g and x = {bob.g, bob.x}")
    print(f"First alice sends hashes to Bob {alice.send_hashes()}")
    bob.listen(alice.send_hashes())
    print(f"Bob generate c and sends to Alice {bob.send_c()}")
    alice.get_c(bob.send_c())
    print(f"Alice sends bob y values: {alice.send_y_values()}")
    bob.get_y_values(alice.send_y_values())
    print(f"Bob verifies the communication with Alice: {bob.verify()}")

    count_of_verified = 0
    for i in range(0, 100):
        alice = Alice()
        bob = Bob()
        bob.listen(alice.send_hashes())
        alice.get_c(bob.send_c())
        bob.get_y_values(alice.send_y_values())
        if bob.verify():
            count_of_verified += 1
    return f"Bob has verified Alice {count_of_verified}/100 times"


def soundness():
    eve = Eve(verbose=True)
    bob = Bob(verbose=True)
    bob.g = eve.g
    bob.x = eve.x
    print(f"Bob knows g and x = {bob.g, bob.x}")
    print(f"First Eve sends hashes to Bob {eve.send_hashes()}")
    bob.listen(eve.send_hashes())
    print(f"Bob generate c and sends to Eve {bob.send_c()}")
    eve.get_c(bob.send_c())
    print(f"Eve sends bob y values: {eve.send_y_values()}")
    bob.get_y_values(eve.send_y_values())
    print(f"Bob verifies the communication with Eve: {bob.verify()}")

    count_of_verified = 0
    for i in range(0, 100):
        alice = Eve()
        bob = Bob()
        bob.listen(eve.send_hashes())
        alice.get_c(bob.send_c())
        bob.get_y_values(eve.send_y_values())
        if bob.verify():
            count_of_verified += 1
    return f"Bob has verified Eve {count_of_verified}/100 times."


def zero_knowledge():
    alice = Alice()
    evan = Evan()
    evan.g = alice.g
    evan.x = alice.x
    print(f"First Alice sends hashes to Evan {alice.send_hashes()}")
    evan.listen(alice.send_hashes())
    print(f"Evan generates c and sends to Alice {evan.send_c()}")
    alice.get_c(evan.send_c())
    print(f"Alice sends Evan y values: {alice.send_y_values()}")
    evan.get_y_values(alice.send_y_values())
    evan.find_the_secrets()
    print(f"Evan verifies the communication with Alice: {evan.verify()}")
    a, b = evan.find_the_secrets()
    return f"Evan found Alice's a = {a} and b = {b} values that should be secret."


print(f"-------------")
print(f"Completeness:")
print(f"If the claim is true, Bob always accepts it.")
print(f"-------------")
print(f"Explanation:")
print(f"""
    Completeness: For this protocol to pass the completeness check
    Alice should be able to prove to Bob that she is Alice given that she has followed the protocol correctly.
    In this example Alice is never able to prove to Bob that she is Alice even though
    she has followed the protocol.
    This is because Bob will check that Alice is who she said she is
    by the equation of y1 ∗ y2 = h1 ∗ h2. But the values of y are calculated as
    y1 = gr1 and y2 = gr2 where r1 = rand(int) and r2 = rand(int), the values for hi are additions of
    c = rand(int) as such that h1 = a + c and h2 = b + c.
    So this equation that Bob checks doesn’t become valid which means that the Completeness checks
    fails since Bob cannot reliably verify Alice.
    
    Example: {completeness()}
""")
print(f"Completeness answer: This protocol is not complete.\n")

print(f"-------------")
print(f"Soundness:")
print(f"Eve cannot convince Bob that statement is true if it is actually false.")
print(f"-------------")
print(f"Explanation:")
print(f"""
    The principle of soundness means that Eve's false claim should be only
    accepted with a very small probability.
    In this example the protocol is clearly not sound,
    because Bob will never accept Legitimate claims by Alice, but will always
    accept Eve's false claims.
    Example: Eve chooses y and h values such that the verification step will pass.
    {soundness()}
""")
print(f"Soundness answer: This protocol is not sound.\n")

print(f"-------------")
print(f"Zero-knowledge:")
print(f"Bob only learns the truth value of the claim and nothing else.")
print(f"-------------")
print(f"Explanation:")
print(f"""
    As taken from the lecture notes of Ahto Puldas:
    There is an efficient simulator M that is able to generate
    the transcript of the protocol (with the same probability distribution as in
    the protocol) knowing only the truth value of the claim.
    Hence, Bob only learns the truth value of the claim, because if he knows
    the truth value, he can simulate the communication himself.
    
    In other words, the prover has to be able to prove that she knows a secret without
    revealing the secret and the verifier has to be able to verify that the prover indeed knows
    the secret without actually being able to see the secret.
    
    So Alice knows a and b values and Bob only knows x value that is composed of the a and b value.
    Bob should not be able to find out the values of a and b to satisfy Zero-knowledge.
    
    Example: Alice starts the protocol with malicious Evan who she thinks is Bob.
    Alice uses her secrets thinking that Evan can't find them out.
    Evan follows the protocol until getting Alices y values and then substracts the c value
    that he sent to Alice to find Alice's secrets.
    But actually:
    {zero_knowledge()}
""")
print(f"Zero-knowledge answer: This protocol doesn't satisfy ZK.")