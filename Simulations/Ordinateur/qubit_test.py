from unittest import TestCase, main
from qubit import *
from calcul import un, zero
from portes import H

class TestQubit:
    def test_ket_zero(self):
        q = Qubit()
        p = Qubit.zero()
        assert q[0] == un
        assert q[1] == zero
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
        assert 3/4 <= l.count(a) / l.count(b) <= 4/3

    def test_multiples_qubits(self):
        q1 = Qubit.zero()
        q2 = Qubit.un()
        q3 = q1 @ q2
        assert q3[0, 0] == zero
        assert q3[0, 1] == un
        assert q3[1, 0] == zero
        assert q3[1, 1] == zero
        assert str(q3) == '1|01⟩'

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


if __name__ == '__main__':
    main()
