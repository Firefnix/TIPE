from portes import *
from qubit import *
from calcul import *

def est_pair(n):
    l = int_vers_bin(n)
    psi = ket(l[-1])
    return (psi @ ket(1)) >> cX

def test_sequence(sequence_attendue, qubit_obtenu):
    val = bra(*sequence_attendue)
    resultat = val | qubit_obtenu
    return resultat == Naturel(1)

def affiche_parite(n):
    if test_sequence([0,1], est_pair(n)):
        print("Le nombre pris en entrée est pair.")
    else:
        print("Le nombre pris en entrée est impair.")

n = int(input("Entrez un nombre entier : "))
affiche_parite(n)
