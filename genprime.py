from primality import probablyPrime
import random
import sys

while True:
    x = random.getrandbits(int(sys.argv[1]))
    if probablyPrime(x):
        print(x)
        break
