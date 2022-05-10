from qubit import ket
from portes import H, I
from calcul import Matrice

N = int(input('Entrez un nombre : '))
N = 12
m = 4
Ei = ket(0) ** (2*m)
G = (H ** m) @ (I ** m)

def f(x: int):
    return (a**x) % N

def decomp(n: int, taille: int):
    l = [ket(0) for i in range(taille)]
    d = [int(i) for i in bin(n)[2:]]
    d = [0] * (taille-len(d)) + d
    q = None
    for i in range(taille):
        if d[i] == 1:
            l[i] = ket(1)
        if q is None:
            q = l[i]
        else:
            q = q @ l[i]
    return q

def recomp(q):
    pass

E = decomp(N, 2*m)

print(G * E)
