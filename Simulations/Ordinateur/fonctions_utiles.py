from portes import H, I
from qubit import bra, ket
from calcul import un, zero, int_vers_bin, int_log2


# Fonction test ordinateur quantique

def sequence_egale(sequence_attendue, qubit_obtenu):
    val = bra(*sequence_attendue)
    resultat = val | qubit_obtenu
    return (2 ** len(sequence_attendue) == qubit_obtenu.dim
            and resultat == un)


# Fonctions raccourcis

def etat_de_base(n_principal, n_auxiliaire, val_auxiliaire = 0):
    return (ket(0) ** n_principal) @ (ket(val_auxiliaire) ** n_auxiliaire)


def ket_vers_liste(q):
    n = q.dim
    for i in range(n):
        if bra(i) | q != zero:
            return int_vers_bin(i, taille=int_log2(n)-1)


# Fonctionne comme range, la fin est exclue
# Si `fin` est négatif on part de la fin
def H_option(total, *, debut, fin):
    assert isinstance(total, int) and isinstance(fin, int)
    assert isinstance(debut, int) and debut >= 0
    if fin < 0:
        fin = total + fin
    return (I ** debut) @ (H ** (fin - debut)) @ (I ** (total -fin))

def qubits_intriques(n, valeur = 0):
    assert isinstance(n, int) and isinstance(valeur, int)
    return (ket(valeur)**n) >> (H**n)
