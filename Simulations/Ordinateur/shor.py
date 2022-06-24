from random import randint
from time import time
import matplotlib.pyplot as plt

from calcul import zero, pgcd, bin_vers_int, int_vers_bin, Naturel
from portes import QFT
from oracle import Oracle
from fonctions_utiles import etat_de_base, H_option, kron_id

m = 4

def main():
    N = int(input('Entrez un nombre : '))
    t0 = time()
    f = facteurs(N, deux_facteurs_shor)
    print('-' * 20)
    print(f"{N} = {' × '.join([str(i) for i in f])}")
    print(f'(calcul effectué en {(time() - t0):.2f} s)')

def facteurs(N, deux_facteurs):
    n, p = deux_facteurs(N)
    if n == 1:
        print(f'| {N} est premier')
        return [N]
    return facteurs(n, deux_facteurs) + facteurs(p, deux_facteurs)

def deux_facteurs_shor(N):
    if N == 2:
        return 1, 2
    print('Décomposition en deux facteurs de', N)
    deja_vus = []
    while True:
        # a = randint(2, N-1)
        a = int(input('NPA : '))
        if a in deja_vus:
            continue
        else:
            deja_vus.append(a)
        d = pgcd(a, N)
        if d != 1:
            print(f'Coup de bol ! {d} divise le NPA {a} et {N}')
            n, p = d, N // d
            return min(n, p), max(n, p)
        print(f'Recherche de période [NPA={a}, N={N}] ...')
        r = periode(a, N)
        print(f'\tLa période obtenue avec le NPA {a} est {r}')
        if r % 2 == 0 and a**(r//2) % N != N-1:
            n = pgcd(a ** (r // 2) + 1, N)
            p = pgcd(a ** (r // 2) - 1, N)
            if n * p == N:
                print(f'C\'est une période valide, {N} = {n} × {p}')
                return min(n, p), max(n, p)
        print('Période invalide, on recommence')

def periode(a, N):
    ef = recherche_periode(a, N)
    demander_affichage(ef)
    for i in range(ef.dim):
        x = ef[i].abs_carre()
        if x != zero:
            inv = x.inverse()
            if not inv.appartient(Naturel):
                raise ValueError(f'la période {inv}, de type {type(inv)} n\'est pas un naturel')
            return int(inv)
    raise ValueError('État final nul')

def cree_f(a, N):
    def f(*bits):
        x = bin_vers_int(*bits)
        return tuple(int_vers_bin((a ** x) % N, taille=m))
    return f

def recherche_periode(a, N):
    U = Oracle.somme(cree_f(a, N), m = m)
    print('\tCréation de l\'état initial ...')
    e0 = etat_de_base(m, m , 0)
    print('\tIntrication des états ...')
    e1 = e0 >> H_option(2*m, debut=0, fin=m)
    print('\tPassage dans l\'oracle ...')
    e2 = e1 >> U
    print('\tCréation du circuit QFT ...')
    Q = QFT(2**m)
    P = kron_id(Q, m)
    print('\tPassage dans le circuit QFT ...')
    e3 = e2 >> P
    return e3

def demander_affichage(ef):
    if input('\tAfficher l\'état final ? [y/n] ') == 'y':
        print('\tL\'état final est :', ef)
    if input('\tAfficher les amplitudes ? [y/n] ') == 'y':
        affiche_amplitudes(ef)

def affiche_amplitudes(ef):
    l = [float(ef[i].abs_carre()) for i in range(ef.dim)]
    x = list(range(ef.dim))
    plt.bar(x, l)
    plt.xlabel('État propre')
    plt.ylabel('Amplitude (module au carré)')
    plt.show()

if __name__ == '__main__':
    main()
