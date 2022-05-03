from random import choices
from calcul import Matrice, un, zero


class EtatPropre:
    def __init__(self, nom):
        # nom est un int ou un str à l'entrée (il est converti en str)
        self.nom = str(nom)

    def __str__(self):
        return '|' + self.nom + '⟩'

    def __and__(self, autre):
        assert isinstance(autre, EtatPropre)
        return EtatPropre(self.nom + autre.nom)

    def __eq__(self, autre):
        # On ne teste pas l'égalité des noms
        return isinstance(autre, EtatPropre) and autre.valeur == self.valeur

    # Change le nom d'un état propre
    def renomme(self, nom):
        self.nom = str(nom)


# L'équivalent d'un Qubit, mais avec d états propres différents
class Qudit:
    # Un Qudit possède d'états possibles
    def __init__(self, dim):
        self.dim = dim
        self.base = [EtatPropre(i) for i in range(dim)]  # vecteurs propres
        self.matrice = Matrice(dim, 1)
        self.matrice[0] = un

    def __eq__(self, autre):
        return self.matrice == autre.matrice

    def __getitem__(self, bras):
        if isinstance(bras, int):
            return self.matrice[bras]
        assert all([(i == 0 or i == 1) for i in bras])
        return self.matrice[
            int(''.join([str(i) for i in bras]), base=2)
        ]

    def __matmul__(self, autre):
        r = Qudit(self.dim * autre.dim)
        r.matrice = self.matrice @ autre.matrice
        for i in range(self.dim * autre.dim):
            nom = bin(i)[2:]
            nom = '0' * ((self.dim * autre.dim)//2 - len(nom)) + nom
            r.base[i].renomme(nom)
        return r

    def mesure(self):
        propres = [Qubit.zero(), Qubit.un()]
        probs = [float(abs(self[i])*abs(self[i])) for i in range(self.dim)]
        choix = choices(list(range(self.dim)), weights = probs)[0]
        for i in range(self.dim):
            self.matrice[i] = zero
        self.matrice[choix] = un
        return self

    def __str__(self):
        return ' + '.join([
            str(self.matrice[i]) + str(self.base[i])
            for i in range(self.dim)
            if self.matrice[i] != zero
        ])


class Qubit(Qudit):
    def __init__(self, c0 = None, c1 = None):
        super().__init__(2)
        if c0 is not None and c1 is not None:
            assert abs(c0) * abs(c0) + abs(c1) * abs(c1) == un
            self.matrice[0] = c0
            self.matrice[1] = c1

    @staticmethod
    def propre(n: int):
        assert n == 0 or n == 1
        if n == 0:
            return Qubit.zero()
        return Qubit.un()

    @staticmethod
    def zero():
        return Qubit()

    @staticmethod
    def un():
        return Qubit(zero, un)

    @staticmethod
    def matrice(m: Matrice):
        assert m.forme == (2, 1)
        q = Qubit()

    def __pow__(self, n: int):
        q = self
        for i in range(n - 1):
            q = q @ self
        return q


def ket(*arg):
    assert all([i == 0 or i == 1 for i in arg])
    q = Qubit.propre(arg[0])
    for i in arg[1:]:
        q = q @ Qubit.propre(i)
    return q


class Bra:
    def __init__(self, *composante):
        print('New bra:', composante)
        self.composante = composante

    def __eq__(self, autre):
        return (isinstance(autre, Bra)
            and self.composante  == autre.composante)

    def __or__(self, q):
        assert isinstance(q, Qudit)
        return q[self.composante]


def bra(*composante):
    return Bra(*composante)
