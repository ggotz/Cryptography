import random
from math import gcd

def fastmodpower (a , n , p ) :
    result = 1
    while n > 0:
        if n % 2 == 1:
            result = result * a % p
        n = n // 2
        a = a * a % p
    return result

def isPrime(n) :
    if n <=1:
        return False
    if n <=3:
        return True
    if n %2==0:
        return False
    q = n -1
    while q % 2 == 0:
        q //=2
    for i in range (30):
        if not RabinMillerTest(n, q):
            return False
    return True

def RabinMillerTest(n , q) :
    a = random.randint(2 , n - 2)
    x = fastmodpower (a ,q , n )
    if x ==1 or x == n -1:
        return True
    while q != n -1:
        x = ( x * x ) % n
        q = 2 * q
        if x == 1:
            return False
        if x == n -1:
            return True
    return False


max_n = 2**20

while True:
    p = random.randint(0, max_n)
    ptonos = (p-1) // 2
    pdistono = (ptonos - 1) // 2
    if pdistono % 4 == 1 and isPrime(pdistono) and isPrime(ptonos) and isPrime(p):
        break

while True:
    q = random.randint(0, max_n)
    qtonos = (q-1) // 2
    qdistono = (qtonos - 1) // 2
    if qdistono % 4 == 1 and isPrime(qdistono) and isPrime(qtonos) and isPrime(q):
        break

print("p =", p, ", q = ", q)

period = 2 * pdistono * qdistono
n = p*q


#find s0
isGood = False
while not isGood:
    isGood = True
    s = random.randint(2, n)

    s = s * s % n
    if gcd(s, n) > 1:
        continue
    factor = [2, pdistono, qdistono, 2 * pdistono, 2 * qdistono,  pdistono * qdistono]
    for d in factor:
        exp = fastmodpower(2, 2 * pdistono * qdistono / d, 2 * ptonos * qtonos)
        if fastmodpower(s, exp, n) == s:
                isGood = False
                break

print("Theoretical period =", period)
cnt = 1
out = s
out = out * out % n

while out != s:
    out = out * out % n
    cnt += 1

print("Experimental period =", cnt)
