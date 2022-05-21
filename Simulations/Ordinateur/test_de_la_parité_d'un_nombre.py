from portes import *
from qubit import *
from calcul import *


def est_pair(n):
    l = int_vers_bin(n)
    Psi = ket(l[-1])
    return (Psi@ket(1)>>cX)



def test_sequence (sequence_attendue,qubit_obtenu):
    val = bra(*sequence_attendue)
    resultat = val | qubit_obtenu
    return(resultat == Naturel(1))



def affiche_parite (n):
    k=test_sequence ([0,1],est_pair(n))
    if k:
        print ("Le nombre pris en entré est pair")
    else:
        print ("Le nombre pris en entré est impair")

