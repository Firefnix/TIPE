class Nombre:
    @staticmethod
    def ou_int(x):
        if isinstance(x, int):
            return Relatif(x).sous()
        return x

    def appartient(self, E):
        return not (self.sur(E) is None)

    def __add__(self, autre):
        T = type(self)
        b = autre.sur(T)
        if b is None:
            return (autre + self).sous()
        return self.plus(b).sous()

    def __mul__(self, autre):
        autre = Nombre.ou_int(autre)
        if isinstance(autre, Matrice):
            return autre * self
        T = type(self)
        b = autre.sur(T)
        if b is None:
            return (autre * self).sous()
        return self.fois(b).sous()

    def __sub__(self, autre):
        return self + (- autre)

    def signe(self):
        return 1 if abs(self) == self else -1

    def __float__(self):
        if isinstance(self, Complexe):
            return float(self.x) + 1j * float(self.y)
        a = self.sur(Puissance)
        return a.sigma * ((a.x.num / a.x.denom) ** (a.p.num / a.p.denom))

    def __truediv__(self, autre):
        autre = Nombre.ou_int(autre)
        return self * autre.inverse()


class Zero(Nombre):
    def __init__(self):
        self.n = 0 # par assimilation aux naturels

    def __eq__(self, autre):
        return isinstance(autre, Zero)

    def __add__(self, autre):
        return autre

    def __mul__(self, autre):
        return self

    def sous(self):
        return self

    def sur(self, E: type):
        return Naturel(0).sur(E)

    def __abs__(self):
        return self

    def __neg__(self):
        return self

    def __str__(self):
        return '0'

zero = Zero()


class Naturel(Nombre):
    def __init__(self, n: int):
        assert n >= 0
        self.n = n

    def __eq__(self, autre):
        return isinstance(autre, Naturel) and autre.n == self.n

    def sous(self):
        if self.n == 0:
            return Zero()
        return self

    def sur(self, E: type):
        if E == Naturel:
            return self
        if E == F2:
            return F2(self.n)
        return Relatif(self.n).sur(E)

    def plus(self, autre):
        return Naturel(self.n + autre.n)

    def fois(self, autre):
        a =  Naturel(self.n * autre.n)
        return a

    def inverse(self):
        return Rationnel(1, self.n).sous()

    def __pow__(self, exposant):
        return self.sur(Relatif) ** exposant

    def __neg__(self):
        return Relatif(- self.n).sous()

    def __abs__(self):
        return self

    def __str__(self):
        return str(self.n)


un = Naturel(1)


class Relatif(Nombre):
    def __init__(self, z: int):
        self.z = z

    def __eq__(self, autre):
        return isinstance(autre, Relatif) and autre.z == self.z

    def sous(self):
        if self.z >= 0:
            return Naturel(self.z).sous()
        return self

    def sur(self, E: type):
        if E == Relatif:
            return self
        return Rationnel(self.z, 1).sur(E)

    def plus(self, autre):
        return Relatif(self.z + autre.z)

    def fois(self, autre):
        return Relatif(self.z * autre.z)

    def __neg__(self):
        return Relatif(- self.z).sous()

    def __abs__(self):
        return Relatif(abs(self.z)).sous()

    def __pow__(self, exposant):
        if exposant.appartient(Naturel):
            return Relatif(self.z ** exposant.n)
        if exposant.appartient(Relatif):
            return Rationnel(un, self ** (- exposant))
        self.sur(Rationnel) ** exposant

    def __str__(self):
        return str(self.z)


class Rationnel(Nombre):
    def __init__(self, num: int, denom: int):
        assert denom != 0
        d = Rationnel._pgcd(abs(num), abs(denom))
        signe = 1 if num * denom >= 0 else -1
        self.num = signe * abs(num) // d
        self.denom = abs(denom) // d

    def __eq__(self, autre):
        return (isinstance(autre, Rationnel)
            and self.num == autre.num
            and self.denom == autre.denom)

    def sous(self):
        if self.denom == 1:
            return Relatif(self.num).sous()
        return self

    def sur(self, E: type):
        if E == Rationnel:
            return self
        sigma = 1 if self.num >= 0 else -1
        return Puissance(
            Rationnel(abs(self.num), self.denom),
            un,
            sigma
        ).sur(E)

    def fois(self, autre):
        return Rationnel(self.num * autre.num,
            self.denom * autre.denom)

    def plus(self, autre):
        return Rationnel(self.num * autre.denom + autre.num * self.denom,
            self.denom * autre.denom).sous()

    def __neg__(self):
        return Rationnel(- self.num, self.denom)

    def __abs__(self):
        return Rationnel(abs(self.num), self.denom)

    def __pow__(self, exposant):
        if exposant == zero:
            return un
        if self.sous() == zero:
            return zero
        if exposant.appartient(Naturel):
            return Rationnel(Relatif(self.num ** exposant.n).z,
                Relatif(self.denom ** exposant.n).z).sous()
        if exposant.appartient(Relatif):
            return (self.inverse() ** (- exposant))

    def inverse(self):
        assert self.num != 0
        return Rationnel(self.denom, self.num)

    @staticmethod
    def _pgcd(a: int, b: int):
        if b == 0:
            return a
        return Rationnel._pgcd(b, a % b)

    def __str__(self):
        return f'{self.num}/{self.denom}'


class Puissance(Nombre):
    def __init__(self, x, p, sigma: int = 1):
        assert sigma == 1 or sigma == -1
        x, p = Nombre.ou_int(x), Nombre.ou_int(p)
        self.x = x.sur(Rationnel)
        assert self.x.num >= 0
        self.p = p.sur(Rationnel)
        self.sigma = sigma

    def __eq__(self, autre):
        autre = autre.sur(Puissance)
        return (autre is not None
            and self.sigma == autre.sigma
            and self.x ** Relatif(self.p.num) == autre.x ** Relatif(autre.p.num)
            and self.p.denom == autre.p.denom)

    def sous(self):
        if self.p.appartient(Relatif):
            return self.sigma * (self.x ** self.p)
        r = self._sous_racine()
        if r is not None:
            return Relatif(self.sigma) * (r ** Relatif(self.p.num).sous())
        return self

    def _sous_racine(self):
        dp = self.p.denom
        for dr in range(1, self.x.denom + 1):
            eta = self.x * Naturel(dr ** dp)
            if eta.appartient(Naturel):
                nr = 0
                while nr ** dp < eta.n:
                    nr += 1
                if nr ** dp == eta.n:
                    return Rationnel(nr, dr)
        return None

    def sur(self, E: type):
        if E == Puissance:
            return self
        if E == Complexe:
            return Complexe(self.sous(), zero)

    def fois(self, autre):
        s = self.sigma * autre.sigma
        if self.x == autre.x:
            return Puissance(self.x, self.p + autre.p, s).sous()
        if self.p == autre.p:
            return Puissance(self.x * autre.x, self.p, s).sous()
        if autre.sous().sur(Rationnel) is not None:
            a = Puissance(abs(autre.sous().sur(Rationnel)), self.p.inverse()).sous().sur(Rationnel)
            if a is not None:
                return Puissance(self.x * a, self.p, self.sigma * autre.signe()).sous()

    def inverse(self):
        assert self.x != zero
        return Puissance(self.x, - self.p, self.sigma)

    def plus(self, autre):
        if autre.sous() == Zero():
            return self

    def __neg__(self):
        return Puissance(self.x, self.p, - self.sigma)

    def __abs__(self):
        return Puissance(self.x, self.p)

    def __str__(self):
        s = '+' if self.sigma == 1 else '-'
        if self.p == Rationnel(1, 2):
            return f'{s}sqrt({str(self.x)})'
        return s + str(self.x) + '^' + str(self.p)


def sqrt(r):
    return Puissance(r, Rationnel(1, 2)).sous()


class Complexe(Nombre):
    def __init__(self, x, y):
        x, y = Nombre.ou_int(x), Nombre.ou_int(y)
        self.x = x.sous()
        self.y = y.sous()

    def __eq__(self, autre):
        return (isinstance(autre, Complexe)
            and self.x == autre.x
            and self.y == autre.y)

    def sous(self):
        if self.y == Zero():
            return self.x
        return self

    def sur(self, E):
        if E == Complexe:
            return self

    def plus(self, autre):
        return Complexe(
            self.x.sous() + autre.x.sous(),
            self.y.sous() + autre.y.sous()
        )

    def fois(self, autre):
        return Complexe(self.x * autre.x - self.y * autre.y,
            self.x * autre.y + self.y * autre.x)

    def __neg__(self):
        return Complexe(- self.x, - self.y)

    def conjugue(self):
        return Complexe(self.x, - self.y).sous()

    # Le module d'un nombre complexe
    def __abs__(self):
        return sqrt(self.x * self.x + self.y * self.y)

    def __str__(self):
        return str(self.x) + '+ i * (' + str(self.y) + ')'


i = Complexe(zero, un)


class F2(Nombre):
    def __init__(self, n):
        if isinstance(n, int):
            self.n = n % 2
        else:
            self.n = n.sous().sur(Relatif).z % 2

    def __eq__(self, autre):
        return isinstance(autre, F2) and self.n == autre.n

    def __int__(self):
        return self.n

    def sous(self):
        return self

    def plus(self, autre):
        return F2((self.n + autre.n) % 2)

    def fois(self, autre):
        return F2(self.n * autre.n)

    def sur(self, E):
        if E == F2:
            return self
        return Naturel(self.n).sur(E)


class Matrice(Nombre):
    # Renvoie une matrice remplie de zéros
    # p est la longueur de la matrice (nombre de lignes)
    # q est la largeur de la matrice (nombre de colonnes)
    def __init__(self, p, q=None):
        if q is None:
            q = p
        assert isinstance(p, int)
        assert isinstance(q, int)
        self.p = p
        self.q = q
        self.forme = (p, q)
        self._c = [[Zero() for _ in range(q)] for _ in range(p)]

    def __eq__(self, autre):
        if self.p != autre.p or self.q != autre.q:
            return False
        for i in range(self.p):
            for j in range(self.q):
                if self[i, j] != autre[i, j]:
                    return False
        return True

    def sur(self, E):
        return None

    def sous(self):
        return self

    @staticmethod
    def tableau(t):
        assert all([len(i) == len(t[0]) for i in t])
        m = Matrice(len(t), len(t[0]))
        m._c = t
        return m

    @staticmethod
    def int_tableau(t):
        assert all([len(i) == len(t[0]) for i in t])
        m = Matrice(len(t), len(t[0]))
        for i in range(len(t)):
            for j in range(len(t[0])):
                m[i, j] = Relatif(t[i][j]).sous()
        return m

    def est_carree(self):
        return self.p == self.q

    def __getitem__(self, item):
        if isinstance(item, tuple):
            i, j = item
            assert isinstance(i, int) and 0 <= i < self.p
            assert isinstance(j, int) and 0 <= j < self.q
            return self._c[i][j]
        assert isinstance(item, int)
        if self.p == 1:
            return self._c[0][item]
        assert self.q == 1
        return self._c[item][0]

    def __setitem__(self, cle, valeur):
        if isinstance(cle, tuple):
            i, j = cle
            assert isinstance(i, int) and 0 <= i < self.p
            assert isinstance(j, int) and 0 <= j < self.q
            assert isinstance(valeur, Nombre)
            self._c[i][j] = valeur
        else:
            assert isinstance(cle, int)
            if self.p == 1:
                self._c[0][cle] = valeur
            else:
                assert self.q == 1
                self._c[cle][0] = valeur

    def _add__(self, autre):
        assert self.p == autre.p
        assert self.q == autre.q
        m = Matrice(self.p, self.q)
        for i in range(self.p):
            for j in range(self.q):
                m[i, j] = self[i, j] + autre[i, j]
        return m

    def __mul__(self, autre):
        if isinstance(autre, Matrice):
            assert self.q == autre.p
            m = Matrice(self.p, autre.q)
            for i in range(self.p):
                for j in range(autre.q):
                    m[i, j] = Zero()
                    for k in range(self.q):
                        m[i, j] += self[i, k] * autre[k, j]
            return m
        m = Matrice(self.p, self.q)
        for i in range(self.p):
            for j in range(self.q):
                m[i, j] = autre * self[i, j]
        return m

    def transposee(self):
        m = Matrice(self.q, self.p)
        for i in range(self.q):
            for j in range(self.p):
                m[i, j] = self[j, i]
        return m

    def conjuguee(self):
        m = Matrice(self.p, self.q)
        for i in range(self.p):
            for j in range(self.q):
                m[i, j] = self[i, j].sur(Complexe).conjugue()
        return m

    @staticmethod
    def scalaire(k, n):
        m = Matrice(n)
        for i in range(n):
            m[i, i] = k
        return m

    @staticmethod
    def identite(n):
        return Matrice.scalaire(un, n)

    # Correspond au produit tensoriel pour deux matrices (prod. de Kronecker)
    # S'utilise pour deux matrices A et B en écrivant A @ B.
    def __matmul__(self, autre):
        assert isinstance(autre, Matrice)
        m = Matrice(self.p * autre.p, self.q * autre.q)
        for i in range(self.p * autre.p):
            for j in range(self.q * autre.q):
                m[i, j] = self[i // autre.p, j // autre.q] * autre[i % autre.p, j % autre.q]
        return m

    def __str__(self):
        n = max([len(str(self[i, j])) for i in range(self.p) for j in range(self.q)])
        return '\n'.join([
            '( ' + ' '.join([
                str(self[i, j]).ljust(n) for j in range(self.q)
            ]) + ' )'
            for i in range(self.p)
        ])


class Eipi(Nombre):
    def __init__(self, arg):
        self._arg = arg

    def arg(self):
        return self._arg

    def sur(self, E: type):
        if E == Eipi:
            return self
        return None

    def __mul__(self, autre):
        if autre == un:
            return self
        if autre == zero:
            return zero

    def __add__(self, autre):
        if autre.sous() == zero:
            return self

    def __str__(self):
        return f'eipi({self.arg()})'
