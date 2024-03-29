from unittest import TestCase, main
from calcul import zero, un

from dj import est_constante, bv
from fonctions_utiles import ket_vers_liste
import pair_impair, parite
from grover import indicatrice, grover, solution


class TestDJ(TestCase):
    def test_constantes(self):
        f = lambda a, b, c, d: zero
        g = lambda a, b, c, d: un
        assert est_constante(f, 4)
        assert est_constante(g, 4)

    def test_equilibrees(self):
        f = lambda a, b, c, d: a
        g = lambda a, b, c, d: a + b
        assert not est_constante(f, 4)
        assert not est_constante(g, 4)


class TestBV(TestCase):
    def test_bv(self):
        a = [zero, un, un]
        b = [zero, zero, un, un]
        assert ket_vers_liste(bv(a)) == [int(i) for i in a]
        assert ket_vers_liste(bv(b)) == [int(i) for i in b]


class TestPairImpair(TestCase):
    def test_pair_impair(self):
        for n in list(range(15)):
            assert pair_impair.est_pair(n) == (n % 2 == 0)

    def test_parite(self):
        for n in list(range(15)):
            assert parite.est_pair(n) == (n % 2 == 0)


class TestGrover:
    def test_grover(self):
        l = ((0, 1, 1), (0, 0))
        for i in l:
            a = grover(*indicatrice(*i))
            assert solution(a) == i


if __name__ == '__main__':
    main()
