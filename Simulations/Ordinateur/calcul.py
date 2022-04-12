class Nombre:
    def appartient(self, E):
        return not (self.sur(E) is None)

    def __add__(self, autre):
        T = type(self)
        b = autre.sur(T)
        if b is None:
            return (autre + self).sous()
        return self.plus(b).sous()

    def __mul__(self, autre):
        if isinstance(autre, Matrice):
            return autre * self
        T = type(self)
        b = autre.sur(T)
        if b is None:
            return (autre * self).sous()
        return self.fois(b).sous()

    def __str__(self):
        return str(type(self))[8:-2].split('.')[-1] + f'({self.aff()})'

    def aff(self):
        return ''


class Zero(Nombre):
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
        return Relatif(self.n).sur(E)

    def plus(self, autre):
        return Naturel(self.n + autre.n)

    def fois(self, autre):
        a =  Naturel(self.n * autre.n)
        return a

    def __pow__(self, exposant):
        return self.sur(Relatif) ** exposant

    def __neg__(self):
        return Relatif(self.n).sous()

    def __abs__(self):
        return self

    def aff(self):
        return self.n


def un():
    return Naturel(1)


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
        return Relatif(self.z).sous()

    def __abs__(self):
        return Relatif(abs(self.z)).sous()

    def __pow__(self, exposant):
        if exposant.appartient(Naturel):
            return Relatif(self.z ** exposant.n)
        if exposant.appartient(Relatif):
            return Rationnel(un(), self ** (- exposant))
        self.sur(Rationnel) ** exposant

    def aff(self):
        return self.z


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
        return Puissance(self, un()).sur(E)

    def fois(self, autre):
        return Rationnel(self.num * autre.num,
            self.denom * autre.denom)

    def __add__(self, autre):
        return Rationnel(self.num * autre.denom + autre.num * self.denom,
            self.denom * autre.denom).sous()

    def __neg__(self):
        return Rationnel(- self.num, self.denom)

    def __abs__(self):
        return Rationnel(abs(self.p), self.q)

    def __pow__(self, exposant):
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

    def aff(self):
        return f'{self.num}/{self.denom}'

class Puissance(Nombre):
    def __init__(self, x, p, sigma: int = 1):
        assert sigma == 1 or sigma == -1
        if isinstance(x, int):
            x = Relatif(x)
        if isinstance(p, int):
            p = Relatif(p)
        self.x = x.sur(Rationnel)
        self.p = p.sur(Rationnel)
        self.sigma = sigma

    def __eq__(self, autre):
        autre = autre.sur(Puissance)
        return (autre is not None
            and self.x ** Relatif(self.p.num) == autre.x ** Relatif(autre.p.num)
            and self.p.denom == autre.p.denom)

    def sous(self):
        if self.p.appartient(Relatif):
            return self.sigma * (self.x ** self.p)
        r = self._sous_racine()
        if r is not None:
            return r ** (Relatif(self.p.num).sous())
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
        return None

    def fois(self, autre):
        if self.x == autre.x:
            return Puissance(self.x, self.p + autre.p).sous()
        if self.p == autre.p:
            return Puissance(self.x * autre.x, self.p).sous()
        if autre == un():
            return self
        if autre == Relatif(-1):
            return Puissance(self.x, self.p, - self.sigma).sous()

    def plus(self, autre):
        pass

    def aff(self):
        return str(self.x) + '^' + str(self.p)


def sqrt(r):
    return Puissance(r, Rationnel(1, 2))


class Complexe(Nombre):
    def __init__(self, x, y):
        if isinstance(x, int):
            x = Relatif(x)
        if isinstance(y, int):
            y = Relatif(y)
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

    def conjugue(self):
        return Complexe(self.x, - self.y).sous()


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
        assert isinstance(item, tuple)
        i, j = item
        assert isinstance(i, int) and 0 <= i < self.p
        assert isinstance(j, int) and 0 <= j < self.q
        return self._c[i][j]

    def __setitem__(self, cle, valeur):
        assert isinstance(cle, tuple)
        i, j = cle
        assert isinstance(i, int) and 0 <= i < self.p
        assert isinstance(j, int) and 0 <= j < self.q
        assert isinstance(valeur, Nombre)
        self._c[i][j] = valeur

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
            m = Matrice(self.p, self.q)
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
                m[i, j] = (m[i, j].sur(Complexe)).conjugue()

    @staticmethod
    def scalaire(k, n):
        m = Matrice(n)
        for i in range(n):
            m[i, i] = k
        return m

    @staticmethod
    def identite(n):
        return Matrice.scalaire(un(), n)

    def __str__(self):
        n = max([len(str(self[i, j])) for i in range(self.p) for j in range(self.q)])
        return '\n'.join([
            '( ' + ' '.join([
                str(self[i, j]).ljust(n) for j in range(self.q)
            ]) + ' )'
            for i in range(self.p)
        ])