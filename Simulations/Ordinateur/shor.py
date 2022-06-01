import random

from calcul import pgcd, bin_vers_int
from qubit import ket
from portes import H, I, QFT
from oracle import Oracle
from fonctions_utiles import etat_de_base, H_option

N = int(input('Entrez un nombre : '))

m = 4
M = 2 ** m
Ei = ket(0) ** (2*m)
G = (H ** m) @ (I ** m)

def cree_f(a):
    def f(b1, b2, b3, b4):
        x = bin_vers_int(b1, b2, b3, b4)
        return (a ** x) % N
    return f

def shor_quantique(m):
    a = random.randint(0, N-1)
    ...
    U = Oracle.somme(cree_f(a))
    e0 = etat_de_base(m, m , 0)
    e1 = e0 >> H_option(2*m, debut=0, fin=m)
    e2 = e1 >> U
    e3 = e2 >> (QFT(m) @ I ** m)
    return e3

print(shor_quantique(m))
