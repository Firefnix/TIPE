import matplotlib.pyplot as plt

from calcul import pgcd, bin_vers_int, int_vers_bin
from qubit import ket
from portes import H, I, QFT
from oracle import Oracle
from fonctions_utiles import etat_de_base, H_option

N = int(input('Entrez un nombre : '))

m = 4
Ei = ket(0) ** (2*m)
G = (H ** m) @ (I ** m)

def cree_f(a):
    def f(b1, b2, b3, b4):
        x = bin_vers_int(b1, b2, b3, b4)
        return tuple(int_vers_bin((a ** x) % N, taille=4))
    return f

def recherche_periode(a, m):
    U = Oracle.somme(cree_f(a), m = 4)
    print('Création de l\'état initial ...')
    e0 = etat_de_base(m, m , 0)
    print('Intraction des états ...')
    e1 = e0 >> H_option(2*m, debut=0, fin=m)
    print('Passage dans l\'oracle ...')
    e2 = e1 >> U
    print('Passage dans QFT ...')
    P = QFT(2**m) @ (I ** m)
    e3 = e2 >> P
    return e3

def affiche_amplitudes(ef):
    l = [float(abs(ef[i])) for i in range(ef.dim)]
    x = list(range(ef.dim))
    plt.bar(x, l)
    plt.xlabel('Rang')
    plt.ylabel('Amplitude')
    plt.show()

ef = recherche_periode(2, 4)
print('L\'état final est :', ef)
affiche_amplitudes(ef)
