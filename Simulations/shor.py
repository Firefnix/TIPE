import random
from statistics import mean, median, stdev
from time import time

def main():
    # On prend un entier N dont on souhaite trouver la décomposition.
    # Pour cela on utilise la fonction facteur, qui donne deux diviseurs de N.
    N = int(input('Entrez un nombre entier : '))
    assert N > 1
    t0 = time()
    f = facteurs(N)
    print(f"{N} = {' × '.join([str(i) for i in f])}")
    print(f'(calcul effectué en {(time() - t0):.2f} s)')

# Renvoie une liste correspodant à la décomposition en facteurs premiers de N
def facteurs(N):
    n, p = deux_facteurs(N)
    if n == 1: # alors p = N est premier (?)
        return [N]
    return facteurs(n) + facteurs(p)

# Revoie un couple de facteurs (n, p) tels que n <= p et N = n * p.
def deux_facteurs(N):
    while True: # tant qu'on ne valide aucune des conditions de retour
        # 1. Prendre un nombre pseudo-aléatoire a < N
        a = random.randint(0, N-1)
        # 2. Calculer le PGCD de a et N
        d = pgcd(a, N)
        if d != 1:
            # 3. a divise N, c'est un facteur de la décomposition de N
            n, p = d, N // d
            return (min(n, p), max(n, p))
        f = lambda x: a**x % N
        r = periode_classique(a, N)
        if r % 2 == 0 and a**(r//2) % N  !=  N-1:
            n = pgcd(a**(r//2)+1, N)
            p = pgcd(a**(r//2)-1, N)
            return (min(n, p), max(n, p))

# Renvoie le PGCD de a et de b en utilisant l'aglorithme d'Euclide.
def pgcd(a, b):
    if a < 0 or b < 0:
        return pgcd(abs(a), abs(b))
    if a == b == 0:
        raise ZeroDivisionError("Le PGCD de 0 et 0 n'est pas défini")
    if b == 0:
        return a;
    elif a == 0:
        return b
    return pgcd(b, a % b)

# Renvoie le plus petit entier r tel que pour tout t entier, f(t + r) = f(t).
def periode_classique(a, N):
    for r in range(1, N):
        if a**r % N == 1:
            return r

# On lance le programme principal
main()
