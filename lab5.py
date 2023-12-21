import hashlib
from lab2 import *
from math import ceil
from sys import byteorder

def sha(n: int) -> int:
    return int.from_bytes(hashlib.sha3_256(n.to_bytes(ceil(n.bit_length() / 8), byteorder=byteorder)).digest(),
                          byteorder=byteorder)

voting_variants = {"Yes" : 1, "No" : 0, "Pass" : 2}

class Server:
    def __init__(self):
        p = random.getrandbits(1024)
        while not is_prime(p):
            p = random.getrandbits(1024)
        q = random.getrandbits(1024)
        while not is_prime(q):
            q = random.getrandbits(1024)

        if p == q:
            return -1
        self.N = p * q
        phi = (p - 1) * (q - 1)
        self.d = get_coPrime(phi)
        self.c = extented_gcd(self.d, phi)[1]

        if self.c < 0:
            self.c += phi
        self.voted = set()

def vote(name, choice):
    print(f"\n${name} голосует")
    rnd = random.getrandbits(512)
    v = voting_variants[choice]
    n = rnd << 512 | v
    r = get_coPrime(a.N)
    h = sha(n)
    h_ = h * rapid_pow(r, a.d, a.N) % a.N

    if name in a.voted:
        print(f"{name} голос уже есть, голоc отклонён")
        return 
    else:
        a.voted.add(name)
        s = rapid_pow(h_, a.c, a.N)

    r_ = extented_gcd(r, a.N)[1]
    if r_ < 0:
        r_ += a.N
    s_ = s * r_ % a.N

    if sha(n) == rapid_pow(s_, a.d, a.N):
        print(f'Голос принят.')

    else:
        print(f'Голос отклонен')
        print(sha(n))
        print(rapid_pow(s_, a.d, a.N))

a = Server()
vote("Alice", "Yes")
vote("Alice", "Yes")
vote("Alice", "Pass")     
vote("Bob", "Yes")
vote("Bob", "No")
vote("Bob", "Pass")        

