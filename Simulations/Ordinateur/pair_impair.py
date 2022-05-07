from portes import Oracle, R, X
from qubit import bra, ket


def f(q):
    return (bra(1) | q).arg() % 2

Uf = Oracle(f)

n = int(input('Entrez un entier : '))

S = ket(0) >> X >> R(n) >> Uf

print('L\'état de sortie est ' + str(S) + '.')
parite = 'pair' if S == ket(0) else 'impair'
print(f'Donc {n} est {parite} !')
