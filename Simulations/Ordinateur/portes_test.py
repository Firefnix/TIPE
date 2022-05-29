from unittest import TestCase, main
from calcul import Matrice, sqrt, un, zero, i
from portes import H, I, X, Y, Z, CNOT, S, Porte, PhaseCond
from qubit import Qubit, ket

class TestPortes(TestCase):
    def test_eq(self):
        assert H == H
        assert I == Porte(Matrice.int_tableau([[1, 0], [0, 1]]))
        assert I != X

    def test_produit_tensoriel(self):
        M = Porte(un / 2 * Matrice.int_tableau([
            [1,  1,  1,  1],
            [1, -1,  1, -1],
            [1,  1, -1, -1],
            [1, -1, -1,  1]
        ]))
        assert H @ H == M

    def test_pow(self):
        assert H ** 3 == H @ H @ H
        assert (I ** 2).matrice == Matrice.identite(4)

    def test_dague(self):
        assert H * H.dague() == I
        assert CNOT * CNOT.dague() == I @ I

    def test_petit_circuit(self):
        C = S * (X @ I) * S * (I @ X)
        assert C.matrice == Matrice.identite(4)
        assert C == I @ I

    def test_droite_a_gauche(self):
        C1 = S * (X @ I) * S * (I @ X)
        C2 = (I @ X) >> S >> (X @ I) >> S
        assert C1 == C2


class TestPortesRemarquables(TestCase):
    def test_identite(self):
        q = Qubit(sqrt(un / 2), sqrt(un / 2))
        assert I * ket(0) == ket(0)
        assert I * ket(1) == ket(1)
        assert I * q == q

    def test_pauli_x(self):
        ket_zero = ket(0)
        ket_un = ket(1)
        assert X * ket_zero == ket_un
        assert X * ket_un == ket_zero

    def test_pauli_y(self):
        p1 = Qubit(zero, i)
        p2 = Qubit(-i, zero)
        assert Y * ket(0) == p1
        assert Y * ket(1) == p2

    def test_pauli_z(self):
        moins_ket_un = Qubit(zero, - un)
        assert Z * ket(0) == ket(0)
        assert Z * ket(1) == moins_ket_un

    def test_hadamard(self):
        z = ket(0)
        u = ket(1)
        q1 = Qubit(sqrt(un / 2), sqrt(un / 2))
        q2 = Qubit(sqrt(un / 2), - sqrt(un / 2))
        assert H * z == q1
        assert H * u == q2

    def test_swap(self):
        q1 = ket(0) >> H
        q2 = ket(1) >> H
        assert (q1 @ q2) >> S == q2 @ q1
        assert (q2 @ q1) >> S == q1 @ q2

    def test_neutre(self):
        # la porte neutre n'est applicable sur aucun qubit
        n = Porte.neutre()
        ph, pi = H ** 0, I ** 0
        assert ph == pi == n
        assert n * n == n == n ** 7
        assert n * (H ** 2) == H ** 2
        assert (H ** 2) * n == H ** 2

    def test_phase_conditionelle(self):
        pc = PhaseCond(3)
        assert ket(0, 0, 0) >> pc == ket(0, 0, 0)
        assert ket(1, 1, 0) >> pc == (- ket(1, 1, 0))


if __name__ == '__main__':
    main()
