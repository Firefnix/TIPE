from calcul import un, zero, i, sqrt, Matrice, Rationnel
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

    def __mul__(self, qubit):
        assert isinstance(qubit, Qubit)
        q = Qubit()
        q.matrice = self.matrice * qubit.matrice
        return q

    def dague(self):
        return Porte(self.matrice.transposee().conjuguee())

    def __matmul__(self, autre):
        assert isinstance(autre, Porte)
        return Porte(self.matrice @ autre.matrice)


I = Identite = Porte(Matrice.int_tableau([[1, 0], [0, 1]]))

H = Hadamard = Porte(
    sqrt(Rationnel(1, 2)) * Matrice.int_tableau([[1, 1], [1, -1]])
)

X = PauliX = Porte(Matrice.int_tableau([[0, 1], [1, 0]]))

Y = PauliY = Porte(Matrice.tableau([[zero, -i], [i, zero]]))

iY = iPauliY = Porte(Matrice.int_tableau([[0, 1], [-1, 0]]))

Z = PauliZ = Porte(Matrice.int_tableau([[1, 0], [0, -1]]))

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
    [0, 0, 1, 0],
]))
