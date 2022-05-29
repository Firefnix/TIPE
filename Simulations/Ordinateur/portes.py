from calcul import un, zero, i, sqrt, Matrice, expi
from qubit import Qudit, bra, ket

class Porte:
    # Une `Porte` s'utilise comme une matrice, en multipliant
    def __init__(self, matrice):
        assert isinstance(matrice, Matrice)
        assert matrice.p == matrice.q
        assert (matrice.p == 1) or matrice.p % 2 == 0
        self.matrice = matrice
        self.taille = matrice.p // 2 # 0 si c'est la porte neutre

    @staticmethod
    def neutre():
        return Porte(Matrice.identite(1))

    def __eq__(self, autre):
        return isinstance(autre, Porte) and self.matrice == autre.matrice

    def __mul__(self, autre):
        if self == Porte.neutre():
            return autre
        if autre == Porte.neutre():
            return self
        if isinstance(autre, Qudit):
            q = Qudit(autre.dim)
            q.matrice = self.matrice * autre.matrice
            return q
        elif isinstance(autre, Porte):
            return Porte(self.matrice * autre.matrice)

    def __rshift__(self, autre):
        return autre * self

    def dague(self):
        return Porte(self.matrice.transposee().conjuguee())

    def __matmul__(self, autre):
        assert isinstance(autre, Porte)
        return Porte(self.matrice @ autre.matrice)

    def __pow__(self, n: int):
        if n == 0:
            return Porte.neutre()
        if self.matrice == Matrice.identite(self.matrice.p):
            return Porte(Matrice.identite(self.matrice.p ** n))
        if self == Porte.neutre():
            return self
        if n == 1:
            return self
        a = self ** (n // 2)
        if n % 2 == 1:
            return self @ (a @ a)
        return a @ a

    def __neg__(self):
        return Porte(- self.matrice)

    def __str__(self):
        return str(self.matrice)

    def __repr__(self):
        return str(self)


I = Identite = Porte(Matrice.int_tableau([[1, 0], [0, 1]]))

H = Hadamard = Porte(sqrt(un / 2) * Matrice.int_tableau([[1, 1], [1, -1]]))

X = PauliX = Porte(Matrice.int_tableau([[0, 1], [1, 0]]))

Y = PauliY = Porte(Matrice.tableau([[zero, -i], [i, zero]]))

iY = iPauliY = Porte(Matrice.int_tableau([[0, 1], [-1, 0]]))

Z = PauliZ = Porte(Matrice.int_tableau([[1, 0], [0, -1]]))

R = lambda phi: Porte(Matrice.tableau([[un, zero], [zero, expi(phi)]]))

S = SWAP = Porte(Matrice.int_tableau([
    [1, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1]
]))

cX = CNOT = Porte(Matrice.int_tableau([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
]))


class OracleDePhase():
    # taille_x: nombre de paramètres pris par f
    def __init__(self, f, taille_x):
        self.f = f
        self.n = taille_x

    def __mul__(self, qudit):
        assert qudit.dim == 2 ** self.n
        r = Qudit(qudit.dim)
        for i in range(qudit.dim):
            r |= bra(i) | (bra(i) | qudit) * (-un) ** self.f(
                *[F2(i) for i in int_vers_bin(i, taille = self.n)])
        return r
