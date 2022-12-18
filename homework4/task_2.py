alice_pub_e = 3
alice_pub_mod = 55


def alices_hash_function(m, mod):
    a, b = m
    return a * b % mod

# Given hashes in the task.

m1, h1 = (12, 6), 8
m2, h2 = (7, 4), 52
m3, h3 = (22, 8), 11

alices_hashes = [
    ((12, 6), 8),
    ((7, 4), 52),
    ((22, 8), 11)]

# Eves message to sign.
eve_m = (6, 11)

# Even calculates the hash.
eve_h = alices_hash_function(eve_m, alice_pub_mod)


def extended_eucleidian(a, b):
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


def phi(n):
    """
    Reference: https://www.doc.ic.ac.uk/~mrh/330tutor/ch05s02.html#:~:text=if%20n%20is%20a%20positive,%CF%86(11)%20%3D%2080
    instead of Fermat's little theorem we use EEA.
    Eulers totient function. This will find a number that is relatively prime to the prime n.
    :param n: prime number n.
    :return: return an integer that is relatively prime to n.
    """
    phi = 1
    for i in range(2, n):
        _gcd = extended_eucleidian(i, n)
        if _gcd[-1][2] == 1:
            phi += 1
    return phi


phi_n = phi(alice_pub_mod)

"d has to satisfy 3 * d = 1 mod phi_n"
"This is based on RSA definition."

priv_key = modular_inverse(alice_pub_e, phi_n)


def sign_message(m, priv_key, mod):
    """
    Function to sign a message.
    :param m:
    :param priv_key:
    :param mod:
    :return:
    """
    return m**priv_key % mod


def task_2():
    """
    Alice decided to use the following hash function together with 
    textbook RSA signature: H:Z×Z→Z∗55 defined by H∶(a,b) → ab mod 55.
    This means that Alice hashes messages of the form m = (a, b)
    and then signs hash with RSA signature. Alice’s public key is (n, e) = (55, 3).
    Malicious Eve wants to obtain signature on bad message m = (6, 11),
    but she cannot interact with Alice and ask her to sign this message.
    Eve listened on communication channel between
    Alice and Bob and intercepted the following message-signature pairs:
    • (m1,σ1)=((12,6),8)
    • (m2,σ2)=((7,4),52)
    • (m3,σ3)=((22,8),11)

    1. Which of these messages will be useful for Eve and why?
    2. What will be signature on message m = (6, 11)?
    """

    print(f"Malicious Eve calculates a hash for {eve_m} based on Alices hashing algorithm")
    print(f"hash = {eve_m[0]}*{eve_m[1]} mod 55 = {eve_h}")
    print(f"Eve checks her has against Alices hashes that she intercepted")
    for hash in alices_hashes:
        print(f"{hash} =? ({eve_m}, {eve_h})")
        if hash[1] == eve_h:
            print(f"this: {hash} = ({eve_m}, {eve_h})")
            print(f"""Eve found that she has the same hash {eve_h} corresponding to Alices message {hash[0]}""")
            print(f"This hash: {eve_h} is useful because"
                  f" Eve can use it as a signature for her own message {eve_m}.")
    print(f"""
To check if Eve actually could use it to sign her own message 
we can see if we can find the private key of Alice and use it to sign Eve's message legitimately.
For this we need to find the value for d (private_key), such that it satisfies: e * d = 1 mod phi(n). Eve knows Alice's
public values for e = {alice_pub_e} and n = {alice_pub_mod}.

RSA private key is generated such that: e * d mod phi(n) = 1 To find the value for d we can 
calculate the multiplicative inverse: d = e^-1 mod phi(n).

Eve also needs to find phi(n) for this she uses Euler's totient function of phi({alice_pub_mod}) = {phi_n}.
Lastly she can now use EEA to find d = e^-1 mod phi(n) = {modular_inverse(alice_pub_e, phi_n)}.

Eve can now use d = {modular_inverse(alice_pub_e, phi_n)} to sign her message.

RSA message signing is done using: 
m_hash^d mod phi(n): {eve_h}^{modular_inverse(alice_pub_e, phi_n)} mod {phi(alice_pub_mod)} = {eve_h**modular_inverse(alice_pub_e, phi_n) % phi(alice_pub_mod)}

Eve didn't really need to find Alice's key, since this can prove that
The signature works.

Alice can verify each hash by: hash^e mod n == m_a * m_b mod n:
    h1: 8^3 mod 55 = {h1**alice_pub_e % alice_pub_mod} == m1: 12 * 6 mod 55 = {m1[0] * m1[1] % alice_pub_mod}
    h2: 52^3 mod 55 = {h2**alice_pub_e % alice_pub_mod} == m2: 7 * 4 mod 55 = {m2[0] * m2[1] % alice_pub_mod}
    h3: 11^3 mod 55 = {h3**alice_pub_e % alice_pub_mod} == m3: 22 * 8 mod 55 = {m3[0] * m3[1] % alice_pub_mod}
    
    Malicious message that works:
    h4: 11^3 mod 55 = {h3**alice_pub_e % alice_pub_mod} == m4: 6 * 11 mod 55 = {eve_m[0] * eve_m[1] % alice_pub_mod}
    
    Malicious message that doesn't work:
    h5: 35^3 mod 55 = {35**alice_pub_e % alice_pub_mod} == m4: 5 * 7 mod 55 = {5 * 7 % alice_pub_mod}
    
    """)
    print(f"Thus we have proven that the signature of Alice's message ({m3}, {h3}) is the same as Eves message ({eve_m}, {eve_h})")


task_2()
