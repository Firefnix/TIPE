from unittest import TestCase, main
from qubit import ket
from portes import H, I
from fonctions_utiles import H_option, ket_vers_liste, etat_de_base, sequence_egale, qubits_intriques


class TestFonctions(TestCase):
    def test_sequence_egale(self):
        e0 = ket(1, 1, 0)
        e1 = ket(1, 0, 0)
        e2 = ket(0, 1, 1, 0)
        assert sequence_egale([1, 1, 0], e0)
        assert not sequence_egale([1, 1, 0], e1)
        assert not sequence_egale([1, 1, 0], e2)

    def test_etat_de_base(self):
        e0 = etat_de_base(2, 1)
        e1 = etat_de_base(2, 1, 0)
        e2 = etat_de_base(2, 1, 1)
        assert e0 == e1 == ket(0, 0, 0)
        assert e2 == ket(0, 0, 1)

    def test_ket_vers_liste(self):
        l1, l2 = [1, 0, 1, 1], [0, 1]
        assert ket_vers_liste(ket(*l1)) == l1
        assert ket_vers_liste(ket(*l2)) == l2

    def test_H_option(self):
        B = I @ H @ (I ** 2)
        assert H_option(4, debut=1, fin=-2) == B
        assert H_option(4, debut=1, fin=2) == B

    def test_qubits_intriques(self):
        assert qubits_intriques(2) == ket(0, 0) >> H**2
        assert qubits_intriques(2, valeur=1) == ket(1, 1) >> H**2


if __name__ == '__main__':
    main()
