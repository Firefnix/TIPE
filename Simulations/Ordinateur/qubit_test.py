from unittest import TestCase, main
from qubit import Qubit, Qudit, ket, bra, Bra, EtatPropre
from calcul import un, zero, Matrice
from portes import H

class TestQubit:
    def test_ket_zero(self):
        q = Qubit()
        p = Qubit.zero()
        assert q[0] == q[(0,)] == un
        assert q[1] == q[(1,)] == zero
        assert p == q

    def test_un(self):
        ket_un = Qubit.un()
        assert ket_un[0] == zero
        assert ket_un[1] == un

    def test_mesure(self):
        a, b = Qubit.un(), Qubit.zero()
        l = [(H * Qubit()).mesure() for _ in range(100)]
        assert a.mesure() == Qubit.un()
        assert b.mesure() == Qubit.zero()
        assert all([i in [a, b] for i in l])
        assert 2/3 <= l.count(a) / l.count(b) <= 3/2

    def test_multiples_qubits(self):
        q = ket(0) @ ket(1)
        assert q[0, 0] == zero
        assert q[0, 1] == un
        assert q[1, 0] == zero
        assert q[1, 1] == zero
        assert str(q) == '1|01⟩'

    def test_pow(self):
        e = ket(0) ** 3
        assert e[0, 0, 0] == un
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    if (i, j, k) != (0, 0, 0):
                        assert e[i, j, k] == zero

    def test_ket(self):
        assert ket(0) == Qubit.zero() == Qubit()
        assert ket(1) == Qubit.un()
        assert ket(0, 0) == Qubit.zero() @ Qubit.zero()
        assert ket(0, 1) == Qubit.zero() @ Qubit.un()
        assert ket(1, 1, 1) == Qubit.un() ** 3

    def test_ket_int(self):
        assert ket(6) == ket(1, 1, 0)
        assert ket(2, 3) == ket(1, 0, 1, 1)

    def test_ket_taille(self):
        assert ket(1, taille=3) == ket(0, 0, 1)
        assert ket(1, 0, 1, taille=1) == ket(1, 0, 1)

    def test_str_ket(self):
        assert str(ket(0, 0)) == '1|00⟩'
        assert str(ket(1, 1, 0)) == '1|110⟩'
        assert str(ket(1, 1, 1, 0)) == '1|1110⟩'

    def test_change_composante(self):
        e0 = ket(1, 0)
        e0 |= bra(0, 0) | un
        e0 |= bra(1, 0) | zero
        assert e0 == ket(0, 0)

    def test_neg(self):
        e0 = ket(1, 0)
        e1 = Qudit(Matrice.colonne(0, 0, -1, 0))
        assert e1 == -e0
        assert e0 == -e1

    def test_dim(self):
        e1 = Qudit(Matrice.colonne(0, 0, -1, 0))
        assert e1.dim == 4


class TestEtatPropre:
    def test_nom(self):
        ket_a = EtatPropre('a')
        ket_0 = EtatPropre(0)
        assert ket_a.nom == 'a'
        assert ket_0.nom == '0'

    def test_renomme(self):
        e = EtatPropre('a')
        assert e.nom == 'a'
        e.renomme('b')
        assert e.nom == 'b'

    def test_str(self):
        e0 = EtatPropre(0)
        e1 = EtatPropre(1)
        assert str(e0) == '|0⟩'
        assert str(e1) == '|1⟩'

    def test_and(self):
        e0, e1 = EtatPropre(0), EtatPropre(1)
        e01 = e0 & e1
        e101 = e1 & e01
        assert str(e01) == '|01⟩'
        assert str(e101) == '|101⟩'


class TestBra(TestCase):
    def test_raccourci(self):
        assert Bra(0) == bra(0)
        assert Bra(1) == bra(1)
        assert Bra(1, 0, 1) == bra(1, 0, 1)

    def test_bra(self):
        assert bra(0) | ket(0) == un
        assert bra(1) | ket(0) == zero
        assert bra(1, 0) | (ket(1) @ ket(0)) == un
        assert bra(1, 1) | (ket(1) @ ket(0)) == zero

    def test_eq(self):
        assert bra(0, 1) == bra(zero, un)

    def test_produit(self):
        mx, my = Matrice.zeros(8, 1), Matrice.zeros(4, 1)
        mx[7] = un
        my[3] = un
        x, y = Qudit(mx), Qudit(my)
        z = x @ y
        for i in range(8):
            for j in range(4):
                if (i, j) != (7, 3):
                    assert bra(i, j) | z == zero
        assert bra(7, 3) | z == un

    def test_ket_bra(self):
        k = ket(0, 1)
        b = bra(1, 1)
        m = Matrice.zeros(4)
        m[1, 3] = un
        assert k * b == m

    def test_bra_vectoriel_bra(self):
        b1 = bra(1, 0)
        b2 = bra(1, 1, 0)
        b3 = bra(1, 0, 1, 1, 0)
        assert b1 @ b2 == b3

    def test_pow(self):
        b0 = bra(0, 0)
        b1 = bra(0, 0, 0, 0, 0, 0)
        b2 = bra(1, 0, 1)
        b3 = bra(1, 0, 1, 1, 0, 1)
        assert b0 ** 3 == b1
        assert b2 ** 2 == b3


if __name__ == '__main__':
    main()
