import random

def modexp(x, y, m) :
    """
    Return x**y % m
    Page 28 in Algorithms, Dasgupta, C. H. Papadimitriou, and U. V. Vazirani p 28
    """
    r = 1
    x = x % m
     
    if (x == 0):
        return 0
 
    while (y > 0):
    
        # y is odd
        if ((y & 1) == 1) :
            r = (r * x) % m
 
        y = y >> 1      
        x = (x * x) % m 
    return r


def probablyPrime(N:int) -> bool:
    def primality(N : int) -> bool:
        """
        This is the primality test from page 27 of Dasgupta. It represents the
        converse of Fermat's Little Theorem.
        :param N:
        :return: False, N is definitely not prime.
                 True, N is prime with probability 1/2.
        """
        a = random.randrange(1,N)
        return modexp(a,N-1,N) == 1

    for i in range(200):
        if primality(N):
            continue
        else:
            return False
    return True