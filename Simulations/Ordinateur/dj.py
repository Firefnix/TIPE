from calcul import un, zero
from fonctions_utiles import qubits_intriques
from portes import H
from oracle import Oracle
from qubit import bra

def dj(f, n):
    q = qubits_intriques(n)
    U = Oracle.phase(f)
    C = q >> U >> (H**n)
    return C

def est_constante(f, n):
    q = dj(f, n)
    test = bra(*([0]*n)) | q
    return (test == un or test == - un)

def point(x_list, a_list):
    n = len(x_list)
    d = zero
    for i in range(n):
        d += (x_list[i]*a_list[i])
    return d

def bv(a):
    return dj(lambda *args: point(args, a), len(a))
