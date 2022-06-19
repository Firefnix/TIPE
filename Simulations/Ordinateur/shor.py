from random import randint
import matplotlib.pyplot as plt

from calcul import pgcd, bin_vers_int, int_vers_bin
from qubit import ket
from portes import H, I, QFT
from oracle import Oracle
from fonctions_utiles import etat_de_base, H_option, kron_id

N = int(input('Entrez un nombre : '))

m = 4

def cree_f(a):
    def f(*bits):
        x = bin_vers_int(*bits)
        return tuple(int_vers_bin((a ** x) % N, taille=m))
    return f

def recherche_periode(a):
    U = Oracle.somme(cree_f(a), m = m)
    print('Création de l\'état initial ...')
    e0 = etat_de_base(m, m , 0)
    print('Intrication des états ...')
    e1 = e0 >> H_option(2*m, debut=0, fin=m)
    print('Passage dans l\'oracle ...')
    e2 = e1 >> U
    print('Création du circuit QFT ...')
    Q = QFT(2**m)
    P = kron_id(Q, m)
    print('Passage dans le circuit QFT ...')
    e3 = e2 >> P
    return e3

def affiche_amplitudes(ef):
    l = [float(abs(ef[i]) ** 2) for i in range(ef.dim)]
    x = list(range(ef.dim))
    plt.bar(x, l)
    plt.xlabel('État propre')
    plt.ylabel('Amplitude (module au carré)')
    plt.show()

a = randint(2, N-1)
print('Nombre pseudo-aléatoire :', a)
ef = recherche_periode(a)
print('L\'état final est :', ef)
affiche_amplitudes(ef)
