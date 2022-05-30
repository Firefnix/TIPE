from unittest import TestCase, main
from calcul import zero, un
from dj import est_constante, bv
from fonctions_utiles import ket_vers_liste

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


if __name__ == '__main__':
    main()
