"""
Task 4. Assume (S, V ) is a secure MAC that is defined over (K, M, T ).
Assume that "Association of Little Santa Helpers" (ALSA)
keeps a database containing records m1, . . . , mn ∈ M of presents requested by children.
To provide integrity for the data the Santa Claus generates
a random secret key k ∈ K and stores tag ti = S(k, mi) alongside record mi for every i = 1, ..., n.
"""
import copy

magical_device = {
   "santa_key": 17,
   "santa_key_prime": 7,
   "mod": 5112
}


def sign(m):
    """
    This is not a secure MAC tag function, it's created to
    demonstrate how having a MAC tag can protect data integrity.
    :param m:
    :return:
    """
    k = magical_device["santa_key"]
    n = magical_device["mod"]
    return int(''.join(str(ord(c)) for c in m)) ** k % n


def verify(m, t):
    """
    MAC tag verification method. All it does is take the message,
    recalculate the tag and check against the provided tag. This is also not
    secure, only good for a demonstration.
    :param m: 
    :param t: 
    :return: 
    """""

    should_be = sign(m)
    if should_be == t:
        print(f"{m} looks ok.")
        return True
    else:
        print(f"agent of ASLA says: Someone has been naughty, {m} tag: {should_be} != {t}")
        return False


# This will be the DB we use.
list_of_wishes = ["dog", "car", "pony", "toy", "doll", "cat"]
db = {}


for i, wish in enumerate(list_of_wishes):
    # We will create a signature on each message in our DB.
    # Before we start testing, this will be our baseline.
    signature = sign(wish)
    db[i] = [wish, signature]


def agent_of_alsa_adds(m, db):
    """
    The agent of ALSA uses this method to inset a
    message to the DB. Santa signs the message before it
    is inserted into the db using the sign(m) function.
    :param m:
    :param db:
    :return:
    """
    # Santa signs it with the sign(m) method.
    tag = sign(m)
    db[len(db)+1] = [m, tag]
    return db


def santa_present_list_sign(db):
    """
    Santa creates a tag of tags using this function.
    :param db:
    :return:
    """
    all_tags = []
    for wish_nr, wish in db.items():
        wish, tag = wish
        all_tags.append(str(tag))
    concat_tags = "".join(all_tags)
    return sign(concat_tags)


def santa_present_list_verify(db, santas_tag):
    """
    Santa verifies the tag of tags using this function.
    :param db:
    :param santas_tag:
    :return:
    """
    current_tag = santa_present_list_sign(db)
    if santas_tag == current_tag:
        print(f"No wish has been altered, {santas_tag} = {current_tag}")
    else:
        print(f"Santa says: Someone has been naughty, {santas_tag} != {current_tag}")


def test_task_one(clean_db):
    """
    Demonstrating that adding a message that is signed gives no errors.
    :param clean_db:
    :return:
    """
    print("\nAn agent of ALSA adds a wish to the list.\n")
    db = copy.deepcopy(clean_db)

    # Agent of ALSA adds to the db and asks Santa to sign the message
    db = agent_of_alsa_adds("bunny", db)

    print("Verification:")
    for k, v in db.items():
        wish, tag = v
        verify(wish, tag)
    print("---")
    return db


def test_task_two(clean_db):
    print("\nAdversary Grinch tries to modify a wish to be something naughty.\n")

    db = copy.deepcopy(clean_db)

    # Change the wish without new tag
    wish, tag = db[1]
    new_wish = "gun"
    db[1] = [new_wish, tag]

    print(f"Verification:")
    for k, v in db.items():
        wish, tag = v
        verify(wish, tag)
    print("---")
    return db


def test_task_three(clean_db):
    print(f"\nAdversary Grinch tries to change a tag of a wish\n")
    db = copy.deepcopy(clean_db)

    # Change the tag without changing wish
    wish, tag = db[2]
    new_tag = 42
    db[2] = [wish, new_tag]

    print(f"Verification:")
    for k, v in db.items():
        wish, tag = v
        verify(wish, tag)
    print("---")
    return db


def test_task_four(clean_db):
    db = copy.deepcopy(clean_db)

    print(f"\nAdversary Grinch tries to add a wish to the list.\n")

    # Add a wish without being detected
    wish = "money"
    tag = 99
    db[len(db)+1] = [wish, tag]

    print(f"Verification:")
    for k, v in db.items():
        wish, tag = v
        verify(wish, tag)
    print("---")
    return db


def test_task_five(clean_db):
    print(f"\nAdversary Grinch tries to remove a wish from the list.\n")

    # Remove a wish without being detected
    db = copy.deepcopy(clean_db)
    removed = db.pop(4)

    print("Verification:")
    for k, v in db.items():
        wish, tag = v
        verify(wish, tag)
    print("---")
    print(f"! Adversary Grinch can removed a present: '{removed[0]}' "
          f"without being detected by the first verificatin. !")
    return db


def test_task_santa_one(clean_db):
    """
    Now testing if grinch can remove a present without Santa noticing.
    :param clean_db:
    :return:
    """
    print(f"\nSanta is checking the db list twice!")
    print(f"BUT! calculates a new tag too late.\n")

    db = copy.deepcopy(clean_db)

    # Santa's tag of tags on his magical device.
    santas_tag = santa_present_list_sign(db)

    # Santa checks if anyone has been naughty before going further.
    santa_present_list_verify(db, santas_tag)
    # If all checks out then he goes on.

    # Agent of ASLA needs to add a new wish to the list.
    # and asks Santa to generate a new tag for it.
    # then verifies the db.
    db = test_task_one(db)

    print(f"Santas tag: {santas_tag}")
    # The Grinch is quick and removes a wish right after an agent
    # of ALSA inserted a wish.
    db = test_task_five(db)

    # Santa generates a new tag of tags and saves it on his magical device.
    santa_present_list_sign(db)

    print(f"Santa didn't catch Grinches attempt to tamper with the db.")


def test_task_santa_two(clean_db):
    """
    Now testing if grinch can remove a present without Santa noticing.
    :param clean_db:
    :return:
    """
    print(f"\nSanta is checking the db list twice!\n")
    db = copy.deepcopy(clean_db)

    # Santa's tag of tags on his magical device.
    santas_tag = santa_present_list_sign(db)

    # Santa checks if anyone has been naughty before going further.
    santa_present_list_verify(db, santas_tag)

    # Agent of ASLA needs to add a new wish to the list.
    # and asks Santa to generate a new tag for it.
    db = test_task_one(db)
    print(f"Santa calculates a new tag")

    print(f"Santas tag: {santas_tag}")
    db = test_task_five(db)
    santa_present_list_verify(db, santas_tag)
    print(f"Santa caught Grinches attempt to tamper with the db.")



test_task_one(db)
test_task_two(db)
test_task_three(db)
test_task_four(db)
test_task_five(db)
test_task_santa_one(db)
test_task_santa_two(db)
