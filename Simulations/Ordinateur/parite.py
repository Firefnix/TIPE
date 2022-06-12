from portes import cX
from qubit import ket
from calcul import int_vers_bin
from fonctions_utiles import sequence_egale


def est_pair(n):
    psi = ket(int_vers_bin(n)[-1])
    s = (psi @ ket(1)) >> cX
    return sequence_egale([0, 1], s)


def affiche_parite(n):
    if est_pair(n):
        print("Le nombre pris en entrée est pair.")
    else:
        print("Le nombre pris en entrée est impair.")

if __name__ == '__main__':
    n = int(input("Entrez un nombre entier : "))
    affiche_parite(n)
