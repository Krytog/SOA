from hashlib import sha256


def get_hash_of_password(password: str):
    return sha256(password.encode('utf-8')).hexdigest()
