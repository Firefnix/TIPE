from qubit import bra, Qudit
from calcul import zero, un, F2, int_vers_bin, sqrt, int_log2

class Oracle:
    @staticmethod
    def phase(f):
        return OracleDePhase(f)

    @staticmethod
    def somme(f):
        return OracleDeSomme(f)


class OracleDePhase:
    # f est une fonction de (F2)^n dans F2
    def __init__(self, f):
        self.f = f

    def __mul__(self, qudit):
        n = int_log2(qudit.dim)-1
        r = Qudit(qudit.dim)
        for i in range(qudit.dim):
            r |= bra(i) | (bra(i) | qudit) * (-un) ** self.f(
                *[F2(i) for i in int_vers_bin(i, taille=n)])
        return r

class OracleDeSomme:
    # f est une fonction de (F2)^n dans F2
    def __init__(self, f):
        self.f = f

    def _trouve_i0(self, psi):
        for i in range(psi.dim):
            if bra(i) | psi != zero:
                return i

    def _coord_y(self, c_non_nul, c_autre):
        a = (c_autre / c_non_nul)
        return sqrt((a*a + un).inverse())

    def _trouve_alpha_beta(self, psi):
        i0 = self._trouve_i0(psi)
        i1 = (i0+1) % psi.dim if i0 % 2 == 0 else (i0-1) % psi.dim
        c = self._coord_y(psi[i0], psi[i1])
        if i0 % 2 == 0:
            alpha = c
            beta = sqrt(un - alpha*alpha)
        else:
            beta = c
            alpha = sqrt(un - beta*beta)
        return alpha, beta

    def _trouve_coord_x(self, alpha, beta, psi):
        n = psi.dim // 2
        if alpha != zero:
            a_inv = alpha.inverse()
            return [a_inv * psi[2*i] for i in range(n)]
        b_inv = beta.inverse()
        return [b_inv * psi[2*i+1] for i in range(n)]

    def __mul__(self, psi):
        alpha, beta = self._trouve_alpha_beta(psi)
        coord_x = self._trouve_coord_x(alpha, beta, psi)
        res = Qudit(psi.dim)
        n = int_log2(psi.dim // 2)-1
        for j in range(2**n):
            fx = self.f(*[F2(i) for i in int_vers_bin(j, taille=n)])
            res |= bra(j, int(fx)) | alpha * coord_x[j]
            res |= bra(j, int(fx + 1)) | beta * coord_x[j]
        return res
