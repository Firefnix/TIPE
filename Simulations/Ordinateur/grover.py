from fonctions_utiles import etat_de_base, H_option
from portes import H, I, PhaseCond
from oracle import Oracle


def grover(f, n, rep):
    e = etat_de_base(n-1, 1, 1) >> (H**n)
    H_op = H_option(n, debut=0, fin=1)
    B = H_op >> (PhaseCond(n-1) @ I) >> H_op
    Uf = Oracle.phase(f, n)
    for i in range(rep):
        e = e >> B >> Uf
    return e


def f(x, y, z):
    return x + y + z


n = 3
res = grover(f, n, 4)
print(res)
