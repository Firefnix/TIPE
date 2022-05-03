from portes import Oracle, R, X
from qubit import ket
from calcul import Eipi

def f(x):
    return x.arg() % 2

Uf = Oracle(f)

n = int(input('Entrez un entier : '))

def psi(n):
    q = ket(1)
    q.matrice[1] = Eipi(n)
    return q

S = Uf * (R(n) * X * ket(0))

print('L\'état de sortie est ' + str(S) + '.')
parite = 'pair' if S == ket(0) else 'impair'
print(f'Donc {n} est {parite} !')
