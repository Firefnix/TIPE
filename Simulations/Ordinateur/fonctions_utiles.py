from portes import Porte, H, I
from qubit import bra, ket
from calcul import un, zero, int_vers_bin, int_log2, Matrice

# Teste si une liste d'entiers correspond à un qubit
# (ne fonctionne évidemment que pour les états propres)
def sequence_egale(sequence_attendue, qubit_obtenu):
    val = bra(*sequence_attendue)
    resultat = val | qubit_obtenu
    return (2 ** len(sequence_attendue) == qubit_obtenu.dim
            and resultat == un)

def etat_de_base(n_principal, n_auxiliaire, val_auxiliaire = 0):
    return (ket(0) ** n_principal) @ (ket(val_auxiliaire) ** n_auxiliaire)

# ne fonctionne que pour les états propres
def ket_vers_liste(q):
    n = q.dim
    for i in range(n):
        if bra(i) | q != zero:
            return int_vers_bin(i, taille=int_log2(n)-1)

# Fonctionne comme range, la fin est exclue.
# Si `fin` est négatif on part de la fin.
def H_option(total, *, debut, fin):
    assert isinstance(total, int) and isinstance(fin, int)
    assert isinstance(debut, int) and debut >= 0
    if fin < 0:
        fin = total + fin
    A = (I ** debut)
    B = (H ** (fin - debut))
    return kron_id(A @ B, total -fin)

# Crée des états propres et les fait tous passer dans une porte de Hadamard.
def qubits_intriques(n, valeur = 0):
    assert isinstance(n, int) and isinstance(valeur, int)
    return (ket(valeur)**n) >> (H**n)

# On fait le calcul `m @ I(n)`, avec I(n) l'identité de taille n,
# et m une matrice quelconque.
# Les analyses montrent que c'est en moyenne 30 fois plus rapide.
def kron_id_mat(m, n):
    r = Matrice.zeros(m.p * n, m.q * n)
    for i in range(m.p):
        for j in range(m.q):
            for k in range(n):
                r[i*n + k, j*n + k] = m[i, j]
    return r

# On calcule la *porte* `P @ (I ** 2)`, avec I l'identité de taille 2.
def kron_id(P, n):
    return Porte(kron_id_mat(P.matrice, 2**n))
