from qubit import bra, ket, Qudit, Qubit
from calcul import zero, un, F2, int_vers_bin, sqrt, int_log2, Matrice, F2Uplet, bin_vers_int

class Oracle:
    @staticmethod
    def phase(f):
        return OracleDePhase(f)

    @staticmethod
    def somme(f):
        return OracleDeSomme(f)

    @staticmethod
    def brut(f):
        return OracleBrut(f)


class OracleBrut:
    def __init__(self, f):
        self.f = f

    def __mul__(self, qudit):
        assert isinstance(qudit, Qudit)
        return ket(self.f(qudit))


class OracleDePhase:
    # f est une fonction de (F2)^n dans F2
    def __init__(self, f):
        self.f = f

    def __mul__(self, qudit):
        n = int_log2(qudit.dim) - 1
        r = Qudit.zero(qudit.dim)
        for i in range(qudit.dim):
            r |= bra(i) | (bra(i) | qudit) * (-un) ** self.f(
                *[F2(i) for i in int_vers_bin(i, taille=n)])
        return r


class OracleDeSomme:
    # f est une fonction de (F2)^n dans (F2)^m
    # par défaut, la taille de y est 1 (f va de (F2)^n dans F2)
    def __init__(self, f, *, m = 1):
        self.f = f
        self.m = m

    def _trouve_i0(self, psi):
        for i in range(psi.dim):
            if bra(i) | psi != zero:
                return i

    def _coord_y(self, c_non_nul, c_autre):
        a = (c_autre / c_non_nul)
        return sqrt((a*a + un).inverse())

    def _trouve_alpha_beta(self, psi):
        i0 = self._trouve_i0(psi)
        i1 = i0+1 if i0 % 2 == 0 else i0-1
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

    def _trouve_x_y(self, psi):
        x, y = psi, None
        for i in range(self.m):
            alpha, beta = self._trouve_alpha_beta(x)
            coord_x = self._trouve_coord_x(alpha, beta, x)
            x = Qudit(Matrice.colonne(coord_x))
            if y is None:
                y = Qubit(alpha, beta)
            else:
                y = y @ Qubit(alpha, beta)
        return x, y


    def __mul__(self, qudit):
        psi = Qudit(
            Matrice([[abs(qudit[i])] for i in range(qudit.dim)]))
        n = int_log2(psi.dim // 2) - self.m
        x, y = self._trouve_x_y(psi)
        res = Qudit.zero(psi.dim)
        res[0] = zero
        for i in range(2**n):
            fx = self.f(*[F2(k) for k in int_vers_bin(i, taille=n)])
            if isinstance(fx, F2): fx = (fx,)
            u = F2Uplet(*fx)
            for j in range(2**self.m):
                v = F2Uplet(*int_vers_bin(j, taille=self.m))
                c = tuple(int_vers_bin(i, taille=n)) + tuple(u + v)
                res[bin_vers_int(*c)] = x[i] * y[j]
        return res
