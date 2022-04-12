from calcul import *
from unittest import TestCase, main

class TestZero(TestCase):
    def test_sous(self):
        assert Zero().sous() == Zero()

    def test_sur(self):
        z = Zero()
        assert z.sur(Naturel) == Naturel(0)
        assert z.sur(Relatif) == Relatif(0)
        assert z.sur(Rationnel) == Rationnel(0, 1)

    def test_plus(self):
        zero = Zero()
        trois = Naturel(3)
        assert zero + zero == zero
        assert trois + zero == trois
        assert zero + trois == trois

    def test_fois(self):
        zero = Zero()
        trois = Naturel(3)
        moins_trois = Relatif(-3)
        un_tiers = Rationnel(1, 3)
        assert zero * zero == zero
        assert zero * trois == zero
        assert trois * zero == zero
        assert zero * moins_trois == zero
        assert moins_trois * zero == zero
        assert zero * un_tiers == zero
        assert un_tiers * zero == zero


class TestNaturels(TestCase):
    def test_sous(self):
        trois = Naturel(3)
        zero = Naturel(0)
        assert trois.sous() == trois
        assert zero.sous() == Zero()

    def test_plus(self):
        deux = Naturel(2)
        trois = Naturel(3)
        cinq = Naturel(5)
        assert deux + trois == cinq
        assert trois + deux == cinq

    def test_fois(self):
        deux = Naturel(2)
        trois = Naturel(3)
        six = Naturel(6)
        assert deux * trois == six
        assert trois * deux == six

class TestRelatifs(TestCase):
    def test_sous(self):
        moins_trois = Relatif(-3)
        trois = Relatif(3)
        zero = Relatif(0)
        assert zero.sous() == Zero()
        assert trois.sous() == Naturel(3)
        assert moins_trois.sous() == moins_trois

    def test_plus(self):
        deux = Relatif(2)
        trois = Relatif(-3)
        moins_un = Relatif(-1)
        assert deux + trois == moins_un
        assert trois + deux == moins_un

    def test_fois(self):
        deux = Relatif(2)
        moins_trois = Relatif(-3)
        moins_six = Relatif(-6)
        assert deux * moins_trois == moins_six
        assert moins_trois * deux == moins_six

class TestRationnels(TestCase):
    def test_sous(self):
        assert Rationnel(0, 3).sous() == Zero()
        assert Rationnel(6, 2).sous() == Naturel(3)
        assert Rationnel(-6, 2).sous() == Relatif(-3)

    def test_eq(self):
        assert Rationnel(2, 6) == Rationnel(1, 3)
        assert Rationnel(1, -3) == Rationnel(-1, 3)
        assert Rationnel(-1, -3) == Rationnel(1, 3)

    def test_neg(self):
        assert (- Rationnel(1, 3)) == Rationnel(-1, 3)
        assert (- (- Rationnel(1, 3))) == Rationnel(1, 3)

    def test_plus(self):
        un_demi = Rationnel(1, 2)
        moins_un_tiers = Rationnel(-1, 3)
        un_sixieme = Rationnel(1, 6)
        assert un_demi + un_demi == un()
        assert un_demi + (-un_demi) == Zero()
        assert un_demi + moins_un_tiers == un_sixieme

    def test_fois(self):
        deux_tiers = Rationnel(2, 3)
        trois_quarts = Rationnel(3, 4)
        un_demi = Rationnel(1, 2)
        assert deux_tiers * trois_quarts == un_demi
        assert trois_quarts * deux_tiers == un_demi
        assert Relatif(-2) * un_demi == Relatif(-1)
        assert un_demi * Relatif(-2) == Relatif(-1)

class TestPuissance(TestCase):
    def test_sous(self):
        assert Puissance(Naturel(4), Rationnel(1, 2)).sous() == Naturel(2)

    def test_eq(self):
        x = Puissance(Naturel(2), Rationnel(2, 3))
        y = Puissance(Naturel(4), Rationnel(1, 3))
        assert x == y

    def test_sqrt(self):
        assert sqrt(2) == Puissance(2, Rationnel(1, 2))
        assert sqrt(5) == Puissance(5, Rationnel(1, 2))

    def test_fois(self):
        assert sqrt(2) * sqrt(2) == Naturel(2)


class TestComplexe(TestCase):
    def test_plus(self):
        z1 = Complexe(1, -2)
        z2 = Complexe(-2, 1)
        z3 = Complexe(-1, -1)
        assert z1 + z2 == z3

    def test_fois(self):
        z1 = Complexe(un(), Relatif(-2))
        z2 = Complexe(Relatif(-2), un())
        z3 = Complexe(Naturel(2), Naturel(5))

class TestMatrice(TestCase):
    def test_zero(self):
        m = Matrice(2, 3)
        for i in range(2):
            for j in range(3):
                assert m[i, j] == Zero()

    def test_setitem(self):
        m = Matrice(2)
        assert m[0, 1] == Zero()
        m[0, 1] = un()
        assert m[0, 1] == un()

    def test_identite(self):
        m = Matrice.identite(3)
        for i in range(3):
            for j in range(3):
                if i == j:
                    assert m[i, j] == un()
                else:
                    assert m[i, j] == Zero()

    def test_tableau(self):
        m = Matrice.tableau([[un(), Zero()], [un(), Zero()]])
        assert m[0, 0] == un()
        assert m[0, 1] == Zero()
        assert m[1, 0] == un()
        assert m[1, 1] == Zero()

    def test_eq(self):
        m1 = Matrice.int_tableau([[1, 0], [0, 1]])
        m2 = Matrice.int_tableau([[1, 0], [0, 1]])
        assert m1 == m2
        assert m1 != Matrice(2)
        assert m1 != Matrice(2, 3)

    def test_fois(self):
        m1 = Matrice.int_tableau([[1, 2], [3, 4]])
        m2 = Matrice.int_tableau([[4, 5], [6, 7]])
        m3 = Matrice.int_tableau([[16, 19], [36, 43]])
        m4 = Matrice.int_tableau([[19, 28], [27, 40]])
        assert m1 * m2 == m3
        assert m2 * m1 ==  m4

if __name__ == '__main__':
    main()