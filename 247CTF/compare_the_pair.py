import hashlib
import secrets
import itertools

salt = "f789bbc328a3d1a3"
hash = "0e902564435691274142490923013038"


def hash_md5(salt,word):
    return hashlib.md5((salt + word).encode()).hexdigest()

for i in itertools.count(start=237700000):
    to_hash = salt + str(i)
    then_hash = hashlib.md5(to_hash.encode()).hexdigest()
    print(f'{to_hash} -> {then_hash}')
    if then_hash[:2] == '0e' and then_hash[2:].isnumeric():
        print("\n\n\nRESULT: ", str(i))
        break
