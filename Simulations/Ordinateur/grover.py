from math import asin, pi, sqrt
import matplotlib.pyplot as plt

from calcul import F2, int_log2, int_vers_bin
from fonctions_utiles import etat_de_base, H_option
from portes import H, I, PhaseCond
from oracle import Oracle

def main():
    ef = grover(*indicatrice(0, 1, 0, 1, 1, 0))
    print('L\'état de sortie est :', ef)
    print('Une solution est', solution(ef))
    affiche_amplitudes(ef)

def grover(f, n, M = 1):
    theta0 = asin(sqrt(M / (2 ** n)))
    rep = int(pi / (4 * theta0))
    H_op = H_option(n, debut=0, fin=-1)
    Uf = Oracle.phase(f)
    e = etat_de_base(n-1, 1, 1) >> (H**n)
    B = H_op >> (PhaseCond(n-1) @ I) >> H_op
    for i in range(rep):
        e = e >> B >> Uf
    return e

def solution(ef):
    s, fm = None, None
    for i in range(ef.dim):
        f = float(ef[i].abs_carre())
        if s is None or fm < f:
            s, fm = i, f
    return tuple(int_vers_bin(s, taille=int_log2(ef.dim)-1))

def affiche_amplitudes(ef):
    l = [float(ef[i].abs_carre()) for i in range(ef.dim)]
    x = list(range(ef.dim))
    plt.bar(x, l)
    plt.xlabel('État propre')
    plt.ylabel('Probabilité (module au carré de l\'amplitude)')
    plt.show()

def indicatrice(*solution):
    def f(*valeurs):
        if valeurs == tuple([F2(i) for i in solution]):
            return F2(1)
        return F2(0)
    return f, len(solution)


if __name__ == '__main__':
    main()
