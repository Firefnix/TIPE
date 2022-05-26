from portes import *
from qubit import *
from calcul import *

# Fonction test ordinateur quantique

def test_sequence (sequence_attendue,qubit_obtenu):
    val = bra(*sequence_attendue)
    resultat = val | qubit_obtenu
    return(resultat == Naturel(1))

# Fonctions raccourcis

def etat_de_base (n_principal,n_auxiliaire,val_auxiliaire):
    return (ket(0) ** n_principal) @ (ket(val_auxiliaire) ** n_auxiliaire)

def ket_vers_list(q):
    n = q.dim
    for i in range (n):
        if bra(i) | q != zero :
            return int_vers_bin(i, taille=int_log2(n)-1)

def H_option (n_qubit, nb_porteH, place_premiere_porte): # normalement devenu fontionnel
    return (I ** (place_premiere_porte - 1)) @ (H**nb_porteH) @ (I ** (n_qubit - nb_porteH - place_premiere_porte + 1))

def qubits_intriques(nb,val):
    return (ket(val)**nb) >> (H**nb)

p = print
