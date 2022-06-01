from unittest import TestCase, main
from calcul import un, F2, Matrice
from qubit import bra, ket, Qudit
from portes import H
from oracle import OracleDePhase, OracleDeSomme


class TestOracles(TestCase):
    def f(self, x, y):
        assert isinstance(x, F2) and isinstance(y, F2)
        return x + y

    def test_phase_propre(self):
        Uf = OracleDePhase(self.f)
        e1, e2 = ket(1, 0), ket(1, 0)
        e2 |= bra(1, 0) | (-un)
        assert e1 >> Uf == e2

    def test_phase_superposition(self):
        Uf = OracleDePhase(self.f)
        e1 = ket(1, 0) >> (H**2)
        e2 = Qudit.matrice(
            (un / 2) * Matrice([[1], [-1], [1], [-1]])
        )
        assert e1 >> Uf == e2

    def test_somme_propre(self):
        Uf = OracleDeSomme(self.f)
        e1 = ket(1, 1, 0)
        e2 = ket(1, 0, 1)
        e3 = ket(1, 0, 0)
        assert e1 >> Uf == e1
        assert e2 >> Uf == e3
        assert e3 >> Uf == e2

    def test_somme_superposition(self):
        Uf = OracleDeSomme(self.f)
        e0 = ket(0)**3 >> H**3
        assert e0 >> Uf == e0


if __name__ == '__main__':
    main()
