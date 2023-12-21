import hashlib

from lab2 import *

def rsa_sign(m: bytearray, b = -1):
    p = prime_generator_pow(12)
    q = prime_generator(p * 50)

    N = p * q
    phi = (p - 1) * (q - 1)

    d = get_coPrime(phi)
    c = extented_gcd(d, phi)[1]

    if c < 0:
        c += phi

    hash = hashlib.md5(m).hexdigest()

    s = [rapid_pow(int(i, 16), c, N) for i in hash]

    if(b != -1):
        hash_b = hashlib.md5(b).hexdigest()
        e = "".join(str(rapid_pow(i, d, N)) for i in s)

        hash_test = "".join(str(int(i, 16)) for i in hash_b)
        
        print(hash_test == s)


    return s



def el_gamal_sign(m: bytearray, b = -1):
    p = generate_p()    #open
    g = generate_g(p)   #open
    
    x = random.randint(1, p - 1)  #Secret Key

    y = rapid_pow(g, x, p)  #Open key A

    hash = hashlib.md5(m).hexdigest()

    k = random.randint(1, p - 1)
    while(extented_gcd(p-1, k)[0] != 1):
        k = random.randint(1, p - 1)

    r = rapid_pow(g, k, p)

    u = [rapid_pow(int(i, 16) - x * r, 1, p - 1) for i in hash]

    s = []
    for i in u:
        temp = extented_gcd(k, p - 1)[1]
        if temp < 0:
            temp += p - 1
        s.append(rapid_pow(temp * i, 1 , p - 1))
    
    sign = ''.join(str(rapid_pow(y, r, p) * rapid_pow(r, i, p) % p) for i in s)
    sign += "1"
    
    if(b == -1):
        sign_b = ''.join(str(rapid_pow(g, int(i, 16), p)) for i in hash)

        print (sign == sign_b)

    return sign

def gost_sign(m:bytearray):
    b = random.getrandbits(20)
    q = random.getrandbits(256)
    p = 2
    while not is_prime(q):
        q = random.getrandbits(256)

    while not is_prime(q * b + 1):
        b = random.getrandbits(20)
        p = q * b + 1

    g = random.randint(1, p - 1)
    a = rapid_pow(g, b, p)
    while a < 2:
        g = random.randint(1, p - 1)
        a = rapid_pow(g, b, p)

    x = random.randint(0, q)
    y = rapid_pow(a, x, p)

    h = hashlib.md5(m).hexdigest()
    h = int(h, 16)

    k = random.randint(0, q)
    r = rapid_pow(a, k, p) % q
    s = (k * h + x * r) % q
    while s == 0:
        k = random.randint(0, q)
        r = rapid_pow(a, k, p) % q
        s = (k * h + x * r) % q

    temp = extented_gcd(h,q)[1]
    if temp < 1:
        temp += q

    u1 = rapid_pow(s * temp, 1, q)
    u2 = rapid_pow(-r * temp, 1, q)

    v = ((rapid_pow(a, u1, p) * rapid_pow(y, u2, p)) % p) % q

    print(v == r)

    return r


        
    
    







    

