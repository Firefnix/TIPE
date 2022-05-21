from portes import *
from qubit import *
from calcul import *

##Fonction test ordinateur quantique


def test_sequence (sequence_attendue,qubit_obtenu):
    val = bra(*sequence_attendue)
    resultat = val | qubit_obtenu
    return(resultat == Naturel(1))


##Fonction raccourcie


def etat_de_base (n_principal,n_auxiliaire,val_auxiliaire):
    return (ket(0) ** n_principal) @ (ket(val_auxiliaire) ** n_auxiliaire)

def nb_vers_ket (n):
    return ket(*int_vers_bin(n))

def H_option (n_qubit,nb_porteH,place_premiere_porte): ##normalement devenu fontionnel
        return (I ** (place_premiere_porte - 1)) @ (H**nb_porteH) @ (I ** (n_qubit - nb_porteH - place_premiere_porte + 1))

def intriqued_qubit(nb,val):
    return (ket(val)**nb) >> (H**nb)

def list_to_ket(l):
    return ket(*l)

def p(a): ##Raccourcie de print pour afficher les test plus rapidement
    print(a)

