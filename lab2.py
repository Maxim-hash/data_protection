from lab1 import *
from math import gcd

keys = {}

def get_coPrime(x):
    y = random.randint(1, x)
    while gcd(x, y) != 1:
        y = random.randint(1, x)

    return y


def shamir_encode(m):
    res= []
    keys['shamir'] = []
    p = prime_generator_pow(9)

    Ca = get_coPrime(p-1)
    Da = extented_gcd(p-1, Ca)[2]

    if Da < 0:
        Da += (p-1)

    Cb =get_coPrime(p-1)
    Db = extented_gcd(p-1, Cb)[2]

    if Db < 0:
        Db += (p-1)
    for part in m:
        x1 = rapid_pow(part, Ca, p)
        x2 = rapid_pow(x1, Cb, p)
        
        x3 = rapid_pow(x2, Da, p)

        res.append(x3)
    
    keys['shamir'] = {'p' : p, 'Ca': Ca, 'Da' : Da, 'Cb' : Cb, 'Db' : Db}
    return res

def shamir_decode(m):
    res = []

    p = keys['shamir']['p']
    Db = keys['shamir']['Db']

    for part in m:
        x4 = rapid_pow(part, Db, p)
        res.append(x4)

    return res

def elgamal_encode(m):
    keys['elgamal'] = []

    res = []
    p = generate_p()
    g= generate_g(p)

    x = random.randint(1, p - 1)
    y = rapid_pow(g, x, p)

    k = random.randint(1, p - 1)
    a = rapid_pow(g, k, p)
    
    for part in m:
        b = part * rapid_pow(y, k, p)
        res.append(b)

    keys['elgamal'] = {'g' : g, 'p' : p, 'x' : x, 'y' : y, 'k' : k, 'a' : a}

    return res

def elgamal_decode(m):
    res = []

    a = keys['elgamal']['a']
    x = keys['elgamal']['x']
    p = keys['elgamal']['p']

    for part in m:
        b = (part * rapid_pow(a, p - 1 - x, p)) % p
        res.append(b)

    return res

def vernam_encode(m):
    res = []
    keys['vernam'] = []
    codes =[random.randint(0, 1023) for _ in range(len(m))]

    keys['vernam'] = codes
    res = [m[i] ^ codes[i] for i in range(len(m))]
    return res

def vernam_decode(m):
    codes = keys['vernam']

    res = [m[i] ^ codes[i] for i in range(len(m))]

    return res

def rsa_encode(m):
    res = []
    keys['rsa'] = []
    p = prime_generator_pow(9)
    q = prime_generator_pow(10)
    n = p * q

    phi = (p - 1) * (q - 1)
    d = get_coPrime(phi)
    c = extented_gcd(d, phi)[1]
    if c < 0:
        c +=phi
    
    for part in m:
        e = rapid_pow(part, d, n)
        res.append(e)

    keys['rsa'].append({'p': p, 'q': q, 'n': n, 'phi': phi, 'd': d, 'c': c})

    return res

def rsa_decode(m):
    res = []
    for key in keys['rsa']:
        n = key['n']
        c = key['c']

    for el in m:
        res.append(rapid_pow(el, c, n))
        
    return res