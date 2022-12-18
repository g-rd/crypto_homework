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


def chinese_remainder_theorem(c, m):
    # first we find the product of the moduli.
    # This is the common modulus.
    M_product = 1

    for m_i in m:
      M_product *= m_i

    result = 0
    # 1. We divide the product of moduli with the modulus m_i
    # 2. we find the multiplicative_inverse of step_1 in mod m_i
    # 3. We multiply step_1 and step_2 together.
    # 4. We add all the results together to find the result to the system of congruences.

    for c_i, m_i in zip(c, m):
      result += (M_product / m_i) * c_i * modular_inverse(M_product / m_i, m_i)

    for c_i, m_i in zip(c, m):
      step_1 = (M_product / m_i)
      step_2 = modular_inverse(step_1, m_i)
      step_3 = step_1 * step_2
      result += step_3

    # 6. We return the value of the result in mod M_product that we found
    return int(result % M_product)


def task_three():
    """
    Alice sends the same invitation to her wedding with Bob to their three friends:
    Albus (with pk1 = (115, 3)),
    Charlie (with pk2 = (58, 3)) and
    Dan (with pk3 = (187, 3)). Invitation m is encrypted using the RSA algorithm.

    Eve was not invited to the wedding but wants to come there,
    she needs to find out address of the wedding venue.
    Eve intercepts all 3 ciphertexts c1 = 18, c2 = 21, c3 = 48.
    Show how can Eve recover the invitation message m without factoring public keys.
    What is plaintext message m?

    :return: Alice's message
    """

    print(f"Alice has sent out wedding invitations to her friends encrypted with RSA.")
    # The first part of the public key
    e = 3
    # e * d = 1 mod phi(n)

    pk1 = 115
    pk2 = 58
    pk3 = 187

    # The ciphertexts
    c1 = 18
    c2 = 21
    c3 = 48

    print(f" -Alice used three keys such that they are (pub_key, e): {pk1, e}, {pk2, e} and {pk3, e}")
    print(f"- Eve intercepted three messages corresponding to previous keys: {c1, c2, c3}")
    print(f"- Eve knows that all three ciphertexts contain the same message.")
    print(f"- Since Eve also knows that those messages are encrypted using RSA she can try to decrypt them")
    print(f"  using the 'Hastad’s Broadcast Attack' that employs the CRT then takes the ")
    print(f"  3rd root of the result of CRT to find the original message.")

    print(f"\nStep one, Eve constructs a system of congruences:")
    print("""
    # Eve constructs the system of congruences such that:
    # ciphertext = message^e mod pub_key
    # message^e = c1 mod pk1
    # message^e = c2 mod pk2
    # message^e = c3 mod pk3
    """)
    print(f"Step two, Eve calculates the result of the system using CRT:"
          f" {chinese_remainder_theorem([c1, c2, c3], [pk1, pk2, pk3])}")
    print(f"Lastly Eve takes the 3rd root of the result and finds the original message: {round(chinese_remainder_theorem([c1, c2, c3], [pk1, pk2, pk3])**(1/3))}")
    print(f"! Eve has successfully decrypted Alices message, she will proceed to crash the wedding !")

    return round(chinese_remainder_theorem([c1, c2, c3], [pk1, pk2, pk3])**(1/3))


task_three()
