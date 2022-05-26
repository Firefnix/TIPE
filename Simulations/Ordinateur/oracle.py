from qubit import bra, ket, Qudit
from calcul import un, F2, int_vers_bin

class Oracle:
    @staticmethod
    def phase(f, taille_x):
        return OracleDePhase(f, taille_x)

    @staticmethod
    def somme(f, taille_x):
        return OracleDeSomme(f, taille_x)


class OracleDePhase:
    # taille_x: nombre de paramètres pris par f
    def __init__(self, f, taille_x):
        self.f = f
        self.n = taille_x

    def __mul__(self, qudit):
        assert qudit.dim == 2 ** self.n
        r = Qudit(qudit.dim)
        for i in range(qudit.dim):
            r |= bra(i) | (bra(i) | qudit) * (-un) ** self.f(
                *[F2(i) for i in int_vers_bin(i, taille=self.n)])
        return r
