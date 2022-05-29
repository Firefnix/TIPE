from portes import cX
from qubit import ket
from calcul import int_vers_bin
from fonctions_utiles import test_sequence


def est_pair(n):
    psi = ket(int_vers_bin(n)[-1])
    return (psi @ ket(1)) >> cX


def affiche_parite(n):
    if test_sequence([0, 1], est_pair(n)):
        print("Le nombre pris en entrée est pair.")
    else:
        print("Le nombre pris en entrée est impair.")


n = int(input("Entrez un nombre entier : "))
affiche_parite(n)
