from portes import R, X
from oracle import Oracle
from qubit import bra, ket


def f(q):
    return (bra(1) | q).arg() % 2

Uf = Oracle.brut(f)

def etat_sortie(n):
    return ket(0) >> X >> R(n) >> Uf

def est_pair(n):
    return etat_sortie(n) == ket(0)

def main():
    n = int(input('Entrez un entier : '))
    S = etat_sortie(n)

    print('L\'état de sortie est ' + str(S) + '.')
    parite = 'pair' if S == ket(0) else 'impair'
    print(f'Donc {n} est {parite} !')

if __name__ == '__main__':
    main()
