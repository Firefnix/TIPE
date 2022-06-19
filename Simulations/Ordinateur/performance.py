import sys
from timeit import timeit
import matplotlib.pyplot as plt

from portes import H, I, QFT
from fonctions_utiles import H_option, kron_id

def temps(entiers, fonction, N = 12):
    t = []
    resultats = []
    for i in entiers:
        rep = 100 if not i else (N // i)
        print(f'Calcul {rep} fois pour n = {i} ...')
        fait = False
        def f():
            nonlocal fait
            if not fait: resultats.append(fonction(i))
            else: fonction(i)
            fait = True
        t.append(timeit(f, number=rep) / rep)
    return t, resultats

def memoire(resultats):
    return [taille(i) for i in resultats]

def perf_pow(M):
    n = [1, 2, 3, 4, 5, 6, 7, 8]
    t, r = temps(n, lambda i: M ** i, N=24)
    return n, t, memoire(r)

def perf_H_option_moins_un():
    n = [1, 2, 3, 4, 5, 6, 7, 9]
    t, r = temps(n, lambda i: H_option(i, debut=0, fin=-1))
    return n, t, memoire(r)

def perf_H_option_moitie():
    n = [1, 2, 3, 4]
    t, r = temps(n, lambda i: H_option(2*i, debut=0, fin=i))
    return n, t, memoire(r)

def perf_qft():
    n = [2, 4, 8, 16]
    t, r = temps(n, lambda i: QFT(i), N=24)
    return n, t, memoire(r)

def perf_shor():
    m = [1, 2, 3, 4, 5]
    t, r = temps(m, lambda i: QFT(2**i) @ (I ** i), N=24)
    return m, t, memoire(r)

def compare_kron_id():
    m = [1, 2, 3, 4, 5]
    M = QFT(16)
    print('Test 1 (classique)')
    t1, _ = temps(m, lambda i: M @ (I ** i))
    print('Test 2 (kron_id)')
    t2, _ = temps(m, lambda i: kron_id(M, i))
    return m, t1, t2

def aff_temps_memoire(n, t, m):
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Entier')

    ax1.plot(n, t, '+', label='Temps (s)', color='orange')
    ax2 = ax1.twinx()
    ax2.plot(n, m, '+', label='Mémoire', color='green')

    fig.legend(loc='upper left', bbox_to_anchor=(0,1), bbox_transform=ax1.transAxes)
    plt.show()

def aff_temps(n, t):
    fig = plt.figure()
    fig.plot(n, t, '+', label='Temps', color='purple')
    fig.xlabel('Entier')
    fig.ylabel('Temps (s)')
    fig.legend()
    plt.show()

def aff_temps1_temps2(n, t1, t2):
    plt.plot(n, t1, '+', label='Temps 1', color='red')
    plt.plot(n, t2, '+', label='Temps 2', color='blue')
    plt.xlabel('Entier')
    plt.ylabel('Temps (s)')
    plt.legend()
    plt.show()

def temps_fmt(t):
    if 1e-6 < t < 1e-3:
        return f'{(t * 1e6):.3g} µs'
    if 1e-3 < t < 1:
        return f'{(t * 1e3):.3g} ms'
    return f'{t:.3g} s'

def nb_fmt(x):
    if isinstance(x, float):
        return f'{x:.2e}'
    return str(x)

def print_donnees(abscisse, *ordonnees):
    ligne = '{:>12}' * len(abscisse)
    print(ligne.format(*abscisse))
    l = zip(*ordonnees)
    for row in l:
        print(ligne.format(*[nb_fmt(i) for i in row]))

def print_ntm(n, t, m):
    print_donnees(
        ['Entier', 'Temps', 'Mémoire'], n,
        [temps_fmt(i) for i in  t], m)

def print_nt(n, t):
    print_donnees(['Entier', 'Temps'], n, [temps_fmt(i) for i in  t])

def print_nt1t2(n, t1, t2):
    N = len(t1)
    print_donnees(
        ['Entier', 'Temps 1', 'Temps 2', 'Rapport'], n,
        [temps_fmt(i) for i in  t1], [temps_fmt(i) for i in  t2],
        [f'{(t1[i]/t2[i]):.3g}' for i in range(N)])
    r_moy = sum(t1[i] / t2[i] for i in range(N)) / N
    print(f'Rapport moyen : {r_moy:.3g}')

def taille(obj):
    if isinstance(obj, list) or isinstance(obj, tuple):
        return sys.getsizeof([]) + sum([taille(i) for i in obj])
    if isinstance(obj, int) or isinstance(obj, bool):
        return sys.getsizeof(obj)
    vus = []
    def aux(o):
        if o in vus: return 0
        vus.append(o)
        s = sys.getsizeof(o)
        return s + sum([taille(i) for i in obj.__dict__.values()])
    return aux(obj)

if __name__ == '__main__':
    n, t1, t2 = compare_kron_id()
    print_nt1t2(n, t1, t2)
    aff_temps1_temps2(n, t1, t2)
