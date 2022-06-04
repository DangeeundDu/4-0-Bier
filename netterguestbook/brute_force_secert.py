import hashlib
import random
from concurrent.futures import ThreadPoolExecutor
from itertools import product
import string

desired_hash = "4fef6f36d4fb3a112aa69bd908eced9a"
sql_query = "SELECT * FROM post WHERE is_public = 1"


def compute_security_hash(secret, value):
    # todo: md5 is deprecated, maybe use hmac in future version?
    return hashlib.md5((secret + value).encode()).hexdigest()


def random_secret():
    return "".join([random.choice(string.printable) for _ in range(10)])


def brute_force_hash():
    while True:
        secret = random_secret()
        hash = compute_security_hash(secret, sql_query)
        if hash == desired_hash:
            print("found valid secret")
            print(secret)


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=6) as exe:
        exe.submit(brute_force_hash())
