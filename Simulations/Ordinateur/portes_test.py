from unittest import TestCase, main
from portes import *

class TestPortes:
    def test_eq(self):
        assert H == H
        assert I == Porte(Matrice.int_tableau([[1, 0], [0, 1]]))
        assert I != X

    def test_identite(self):
        q = Qubit(sqrt(Rationnel(1, 2)), sqrt(Rationnel(1, 2)))
        assert I * Qubit.zero() == Qubit.zero()
        assert I * Qubit.un() == Qubit.un()
        assert I * q == q

    def test_pauli_x(self):
        ket_zero = Qubit.zero()
        ket_un = Qubit.un()
        assert X * ket_zero == ket_un
        assert X * ket_un == ket_zero

    def test_pauli_y(self):
        p1 = Qubit(zero, i)
        p2 = Qubit(-i, zero)
        assert Y * Qubit.zero() == p1
        assert Y * Qubit.un() == p2

    def test_pauli_z(self):
        moins_ket_un = Qubit(zero, - un)
        assert Z * Qubit.zero() == Qubit.zero()
        assert Z * Qubit.un() == moins_ket_un

    def test_hadamard(self):
        z = Qubit.zero()
        u = Qubit.un()
        q1 = Qubit(sqrt(Rationnel(1, 2)), sqrt(Rationnel(1, 2)))
        q2 = Qubit(sqrt(Rationnel(1, 2)), - sqrt(Rationnel(1, 2)))
        assert H * z == q1
        assert H * u == q2

    def test_produit_tensoriel(self):
        M = Porte(Rationnel(1, 2) * Matrice.int_tableau([
            [1,  1,  1,  1],
            [1, -1,  1, -1],
            [1,  1, -1, -1],
            [1, -1, -1,  1]
        ]))
        assert H @ H == M

    def test_dague(self):
        assert H.matrice * H.dague().matrice == I.matrice

if __name__ == '__main__':
    main()
