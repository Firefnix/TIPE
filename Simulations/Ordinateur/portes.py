from calcul import un, i, sqrt, Matrice, expi, Expi, pi
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
        return _neutre

    def __eq__(self, autre):
        return isinstance(autre, Porte) and self.matrice == autre.matrice

    def __mul__(self, autre):
        if self == Porte.neutre():
            return autre
        if autre == Porte.neutre():
            return self
        if isinstance(autre, Qudit):
            return Qudit.matrice(self.matrice * autre.matrice)
        elif isinstance(autre, Porte):
            return Porte(self.matrice * autre.matrice)
        raise TypeError(f'{autre} n\'est ni une porte chaînable ni un qudit')

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


_neutre = Porte(Matrice.identite(1))

I = Identite = Porte(Matrice.tableau([[1, 0], [0, 1]]))

H = Hadamard = Porte(sqrt(un / 2) * Matrice.tableau([[1, 1], [1, -1]]))

X = PauliX = Porte(Matrice.tableau([[0, 1], [1, 0]]))

Y = PauliY = Porte(Matrice.tableau([[0, -i], [i, 0]]))

iY = iPauliY = Porte(Matrice.tableau([[0, 1], [-1, 0]]))

Z = PauliZ = Porte(Matrice.tableau([[1, 0], [0, -1]]))

R = lambda phi: Porte(Matrice.tableau([[1, 0], [0, expi(phi)]]))

PhaseCond = lambda n: Porte((ket(0) ** n) * (bra(0) ** n) * 2 - (Matrice.identite(2**n)))

S = SWAP = Porte(Matrice.tableau([
    [1, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1]
]))

cX = CNOT = Porte(Matrice.tableau([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
]))
