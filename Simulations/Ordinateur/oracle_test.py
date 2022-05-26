from unittest import TestCase, main
from calcul import un, F2, Matrice
from portes import H
from oracle import *


class TestOracles:
    def f(self, x, y):
        assert isinstance(x, F2) and isinstance(y, F2)
        return x + y

    def test_phase_propre(self):
        Uf = OracleDePhase(self.f, 2)
        e1, e2 = ket(1, 0), ket(1, 0)
        e2 |= bra(1, 0) | (-un)
        assert e1 >> Uf == e2

    def test_phase_superposition(self):
        Uf = OracleDePhase(self.f, 2)
        e1 = ket(1, 0) >> (H**2)
        e2 = Qudit.matrice(
            (un / 2) * Matrice.int_tableau([[1], [-1], [1], [-1]])
        )
        assert e1 >> Uf == e2


if __name__ == '__main__':
    main()
