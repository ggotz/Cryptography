import random
import hashlib

# a**n mod p
def fastmodpower(a, n, p):
  result = 1
  while n > 0:
    if n % 2 == 1:
      result = result * a % p
    n = n // 2
    a = a * a % p
  return result

# Primality test (If a number passes 30 times the Rabin-Miller Primality Test, then it is considered as prime)
def isPrime(n):
  if n<=1:
    return False
  if n<=3:
    return True
  if n%2==0:
    return False
  q = n -1
  while q % 2 == 0:
    q//=2
  for _ in range (30):
    if not RabinMillerTest(n,q):
      return False
  return True

def RabinMillerTest(n, q):
  a=random.randint(2, n-2)
  x=fastmodpower(a,q,n)
  if x==1 or x==n-1:
    return True
  while q != n-1:
    x = (x * x) % n
    q = 2 * q
    if x == 1:
      return False
    if x==n-1:
      return True
  return False


# Given two primes p, q and a generator g of group with order q
# We choose a random number as secret key, and we compute the public key as well
def generateKey(p, q, g):
    x = random.randint(2, q-2)
    return fastmodpower(g, x, p), x


# Compute hash of a file that contains a message m
def get_hash_from_file(filename):
  
  with open(filename) as f:
    m = f.read()

  sha512 = hashlib.sha512()
  sha512.update(m.encode("ascii"))
  hm = sha512.hexdigest()

  return hm

# Create a valid sign for the message in file filename
def  sign(filename, g, p, q, pk, sk):
    t = random.randint(1, q - 1)
    T = fastmodpower(g, t, p)
    
    m = get_hash_from_file(filename)

    H = hashlib.sha512()

    H.update(str(T).encode("ascii"))
    H.update(str(pk).encode("ascii"))
    H.update(m.encode("ascii"))
    c = H.hexdigest()

    c = int(c, 16) % q
    # c = H(T||pk||m)
    s = (t + c * sk) % q

    return T, s

# Check if (T, s) is a valid sign for the message in filename
def validate(filename, g, pk, T, s):
    #c = H(T||pk||m)
    m = get_hash_from_file(filename)

    H = hashlib.sha512()

    H.update(str(T).encode("ascii"))
    H.update(str(pk).encode("ascii"))
    H.update(m.encode("ascii"))

    c = H.hexdigest()
    c = int(c, 16) % q

    tmp1 = fastmodpower(g, s, p) 
    tmp2 = (T * fastmodpower(pk, c, p)) % p
    
    if tmp1 == tmp2:
      return True
    return False


# Main 
# Security parameter
N = 512


# Find two primes p, q (where p = 2q + 1)
primeNotFound = True

while primeNotFound:
  q = random.randint(2**(N-1), 2**N)
  if isPrime(q) and isPrime(2 * q + 1):
    primeNotFound = False

p = 2 * q + 1

# Find a number g with order q in Zp
generatorNotFound = True

while generatorNotFound:
  g = random.randint(2, p-1)
  if fastmodpower(g, q, p) == p-1:
    generatorNotFound = False

g = fastmodpower(g, 2, p)

# Key generation
pk, sk = generateKey(p, q, g)

# Sign the message
T, s = sign("mes.txt", g, p, q, pk, sk)

# Check if the created signature is actually valid
if validate("mes.txt", g, pk, T, s):
  print("Valid signature")
else:
  print("Invalid signature")
