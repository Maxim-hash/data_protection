import math
import random

class Person:
    def __init__(self, p, g):
        self.p = p
        self.g = g

    def generate_y(self):
        self.x = random.randint(1, self.p)
        self.y = rapid_pow(self.g, self.x, self.p)

    def generate_z(self, y):
        self.z = rapid_pow(y, self.x, self.p)

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z    


def to_bin(x : int) -> list:
    bin = []
    if x == 0:
        bin.append(0) 
        return bin 
    
    while(x != 0):
        bin.append(x & 1)
        x = x >> 1
    return bin



def is_prime(n) -> bool:
    for x in range(1, 5):
        if(pow(random.randrange(n-1) + 1, (n - 1), n) != 1):
            return False
    return True


def prime_generator_pow(x) -> int:
    if x <= 0: 
        return 1
    p = pow(10, x) + 1
    while True:
        if(is_prime(p)):
            return p
        else:
            p += 2

def prime_generator(x):
    p = x
    if p % 2 == 0: 
        p += 1
    else:
        p += 2
    while True:
        if(is_prime(p)):
            return p
        else:
            p += 2

 
#for i in range(0, 16):
    #print(prime_generator(i))
    #bin = to_bin(i)
    #print(bin)
    #s = 0
    #for j in range(len(bin)):
    #    s += bin[j] * pow(2, j)
    #print(s)


def rapid_pow(a, x : int, p):
    temp_arr = []
    temp_arr.append(a % p)
    bin_x = to_bin(x)

    for i in range(1, len(bin_x)):
        temp_arr.append((temp_arr[i-1] * temp_arr[i-1]) % p)
        
    y = 1

    for i in range(len(bin_x)):
        if bin_x[i] != 0:
            y *= temp_arr[i]

    y %= p

    return y

def extented_gcd(a, b):
    u = [a, 1, 0]
    v = [b, 0, 1]
    while(v[0] != 0):
        q = u[0] // v[0]
        t = [u[0] % v[0], u[1] - q*v[1], u[2] - q*v[2]]
        u = v
        v = t

    return u


def diffi_hellman():
    p = generate_p()
    
    g = generate_g(p)

    A = Person(p, g)
    B = Person(p, g)

    A.generate_y()
    B.generate_y()

    A.generate_z(B.get_y())
    B.generate_z(A.get_y())

    zab = A.get_z()
    zba = B.get_z()

    return zab, zba
        
def generate_p():
    q = prime_generator_pow(12)
    p = 2 * q + 1
    while (not is_prime(p) or not is_prime(q)):
        q = prime_generator(random.randint(q, q * 2))
        p = 2 * q + 1

    return p

def generate_g(p):
    q = int((p - 1) / 2)
    while True:
        for i in range(2, p - 1):

            if(rapid_pow(i, q, p) != 1):
                return i
        else:
            q = prime_generator(q)
            p = 2 * q + 1

def step_by_step(a, p, y):
    x = -1

    m = math.ceil(math.sqrt(p))
    k = math.ceil(math.sqrt(p))

    baby = {rapid_pow(a, i, p) * y % p : i for i in range(m)}
    giant = [rapid_pow(a, i * m, p) for i in range(1, k + 1)]

    for i, value in enumerate(giant, 1):
        j = baby.get(value)
        if j is not None:
            x = i * m - j        
            return x
    return None
