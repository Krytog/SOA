from hashlib import sha256
import random
import string


def get_salt(length):
    output = ""
    for _ in range(length):
        output.join(random.choice(string.ascii_letters))
    return output


def get_hash_of_password(password: str, salt : str):
    str_to_hash = salt + " " + password
    return sha256(str_to_hash.encode('utf-8')).hexdigest()


def is_password_valid(password: str, hashed: str):
    hash, salt = hashed.split(" ")
    return get_hash_of_password(password, salt) == hash