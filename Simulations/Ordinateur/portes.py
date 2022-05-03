from calcul import un, zero, i, sqrt, Matrice, Rationnel, Eipi
from qubit import Qubit

class Porte:
    # Une `Porte` s'utilise comme une matrice, en multipliant
    def __init__(self, matrice):
        assert isinstance(matrice, Matrice)
        assert matrice.p == matrice.q
        assert matrice.p % 2 == 0
        self.matrice = matrice
        self.taille = matrice.p // 2

    def __eq__(self, autre):
        return isinstance(autre, Porte) and self.matrice == autre.matrice

    def __mul__(self, autre):
        if isinstance(autre, Qubit):
            q = Qubit()
            q.matrice = self.matrice * autre.matrice
            return q
        elif isinstance(autre, Porte):
            return Porte(self.matrice * autre.matrice)

    def dague(self):
        return Porte(self.matrice.transposee().conjuguee())

    def __matmul__(self, autre):
        assert isinstance(autre, Porte)
        return Porte(self.matrice @ autre.matrice)

    def __str__(self):
        return str(self.matrice)

    def __pow__(self, n: int):
        p = self
        for i in range(n - 1):
            p = p @ self
        return p



I = Identite = Porte(Matrice.int_tableau([[1, 0], [0, 1]]))

H = Hadamard = Porte(
    sqrt(Rationnel(1, 2)) * Matrice.int_tableau([[1, 1], [1, -1]])
)

X = PauliX = Porte(Matrice.int_tableau([[0, 1], [1, 0]]))

Y = PauliY = Porte(Matrice.tableau([[zero, -i], [i, zero]]))

iY = iPauliY = Porte(Matrice.int_tableau([[0, 1], [-1, 0]]))

Z = PauliZ = Porte(Matrice.int_tableau([[1, 0], [0, -1]]))

R = lambda phi: Porte(Matrice.tableau([[un, zero], [zero, Eipi(phi)]]))

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

class Oracle:
    def __init__(self, f):
        self.f = f

    def __mul__(self, qubit):
        return Qubit.propre(self.f(qubit[1]))
