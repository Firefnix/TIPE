class Nombre:
    @staticmethod
    def ou_int(x):
        if isinstance(x, int):
            return Relatif(x).sous()
        return x

    def sur(self, E: type):
        if E == type(self):
            return self
        if not self.peut_sur(E):
            return None
        if hasattr(self, '_sur'):
            return self._sur(E)

    def appartient(self, E):
        return not (self.sur(E) is None)

    def peut_sur(self, E):
        T = type(self)
        d = {
            F2: [Naturel, Relatif, Rationnel, Puissance, Complexe],
            Naturel: [F2, Relatif, Rationnel, Puissance, Complexe],
            Relatif: [F2, Rationnel, Puissance, Complexe],
            Rationnel: [Puissance, Complexe],
            Puissance: [Complexe],
            Complexe: [Expi],
            Expi: [Complexe]
        }
        return E in d[T] if T in d else False

    def __add__(self, autre):
        T = type(self)
        autre = Nombre.ou_int(autre)
        if isinstance(autre, Somme):
            return autre + self
        if self == zero:
            return autre
        if autre == zero:
            return self
        b = autre.sur(T)
        if b is None:
            return (autre + self).sous()
        return self.plus(b).sous()

    def __add__(self, autre):
        T = type(self)
        autre = Nombre.ou_int(autre)
        if self == zero:
            return autre
        if autre == zero:
            return self
        b = autre.sur(T)
        if b is None:
            return (autre + self).sous()
        return self.plus(b).sous()

    def __mul__(self, autre):
        autre = Nombre.ou_int(autre)
        if self == zero or autre == zero:
            return zero
        if isinstance(autre, Matrice) or isinstance(autre, Somme):
            return autre * self
        T = type(self)
        b = autre.sur(T)
        if b is None:
            return (autre * self).sous()
        return self.fois(b).sous()

    def __sub__(self, autre):
        return self + (- autre)

    def signe(self):
        return 1 if abs(self) == self.sous() else -1

    def __float__(self):
        if isinstance(self, Complexe):
            return float(self.x) + 1j * float(self.y)
        if isinstance(self, Expi):
            return float(abs(self)) ** (1j * float(self.arg()))
        a = self.sur(Puissance)
        if a is not None:
            return a.sigma * ((a.x.num / a.x.denom) ** (a.p.num / a.p.denom))
        raise NotImplementedError

    def __truediv__(self, autre):
        autre = Nombre.ou_int(autre)
        return self * autre.inverse()

    def __repr__(self):
        return str(self)

    def arg(self):
        if self.signe() == 1:
            return zero
        return pi

class MultiplicationErreur(ArithmeticError):
    def __init__(self, n1, n2, message = None):
        self.message = message or f'Multiplication impossible: {n1} * {n2}'
        self.message += ' (types: ' + str(type(n1))[8:-2] + ' et ' + str(type(n2))[8:-2] + ')'
        super().__init__(self.message)

class AdditionErreur(ArithmeticError):
    def __init__(self, n1, n2, message = None):
        self.message = message or f'Addition impossible: {n1} + {n2}'
        self.message += ' (types: ' + str(type(n1))[8:-2] + ' et ' + str(type(n2))[8:-2] + ')'
        super().__init__(self.message)


class Naturel(Nombre):
    def __init__(self, n: int):
        assert n >= 0
        self.n = n

    def __eq__(self, autre):
        return isinstance(autre, Naturel) and autre.n == self.n

    def __int__(self):
        return self.n

    def sous(self):
        return self

    def _sur(self, E: type):
        if E == F2:
            return F2(self.n)
        return Relatif(self.n).sur(E)

    def plus(self, autre):
        return Naturel(self.n + autre.n)

    def fois(self, autre):
        return Naturel(self.n * autre.n)

    def inverse(self):
        return Rationnel(un, self.n)

    def __mod__(self, autre):
        return Naturel(int(self) % int(autre)).sous()

    def __floordiv__(self, autre):
        return Relatif(self.n // int(autre)).sous()

    def __pow__(self, exposant):
        return self.sur(Relatif) ** exposant

    def __neg__(self):
        return Relatif(- self.n).sous()

    def __abs__(self):
        return self

    def __str__(self):
        return str(self.n)


class Relatif(Nombre):
    def __init__(self, z: int):
        self.z = z

    def __eq__(self, autre):
        return isinstance(autre, Relatif) and autre.z == self.z

    def __int__(self):
        return self.z

    def sous(self):
        if self.z >= 0:
            return Naturel(self.z)
        return self

    def _sur(self, E):
        return Rationnel(self.z, 1).sur(E)

    def plus(self, autre):
        return Relatif(self.z + autre.z)

    def fois(self, autre):
        return Relatif(self.z * autre.z)

    def inverse(self):
        return Rationnel(self.signe(), abs(self.z)).sous()

    def __mod__(self, autre):
        return Relatif(int(self) % int(autre)).sous()

    def __floordiv__(self, autre):
        return Relatif(self.z // int(autre)).sous()

    def __neg__(self):
        return Relatif(- self.z).sous()

    def __abs__(self):
        return Naturel(abs(self.z))

    def __pow__(self, exposant):
        exposant = Nombre.ou_int(exposant)
        if exposant.appartient(Naturel):
            return Relatif(self.z ** int(exposant)).sous()
        if exposant.appartient(Relatif):
            return Rationnel(
                un,
                self.z ** abs(int(exposant))
            ).sous()
        return self.sur(Rationnel) ** exposant

    def __str__(self):
        return str(self.z)


zero = Naturel(0)
un = Naturel(1)


def pgcd(a, b) -> int:
    a, b = abs(int(a)), abs(int(b))
    if b == 0:
        return a
    return pgcd(b, a % b)


class Rationnel(Nombre):
    def __init__(self, num: int, denom: int):
        assert denom != 0
        num, denom = int(num), int(denom)
        d = pgcd(abs(num), abs(denom))
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

    def _sur(self, E):
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

    def signe(self):
        return 1 if self.num >= 0 else -1

    def __pow__(self, exposant):
        exposant = Nombre.ou_int(exposant)
        if exposant == zero:
            return un
        if self.sous() == zero:
            return zero
        if exposant.appartient(Naturel):
            return Rationnel(Relatif(self.num ** exposant.n).z,
                             Relatif(self.denom ** exposant.n).z).sous()
        if exposant.appartient(Relatif):
            return self.inverse() ** (- exposant)
        raise ArithmeticError(f'Exponentiation impossible: {self}**{exposant}')

    def inverse(self):
        assert self.num != 0
        return Rationnel(self.denom, self.num).sous()

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
        autre = Nombre.ou_int(autre).sur(Puissance)
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

    def _sur(self, E: type):
        if E == Complexe:
            return Complexe(self.sous(), zero)

    def fois(self, autre):
        s = self.sigma * autre.sigma
        if self.x == autre.x:
            return Puissance(self.x, self.p + autre.p, s).sous()
        if self.x == autre.x.inverse():
            return Puissance(self.x, self.p - autre.p, s).sous()
        if self.p == autre.p:
            return Puissance(self.x * autre.x, self.p, s).sous()
        if autre.sous().sur(Rationnel) is not None:
            a = Puissance(abs(autre.sous().sur(Rationnel)), self.p.inverse()).sous().sur(Rationnel)
            if a is not None:
                return Puissance(self.x * a, self.p, self.sigma * autre.signe()).sous()
        raise MultiplicationErreur(self, autre)

    def inverse(self):
        assert self.x != zero
        return Puissance(self.x, - self.p, self.sigma)

    def plus(self, autre):
        if autre == -self:
            return zero
        if autre == self:
            return self * 2
        return Somme(self.sous(), autre.sous(), feuille=True)

    def __neg__(self):
        return Puissance(self.x, self.p, - self.sigma)

    def __abs__(self):
        return Puissance(self.x, self.p)

    def __str__(self):
        s = '' if self.sigma == 1 else '-'
        if self.p == Rationnel(1, 2):
            return f'{s}sqrt({str(self.x.sous())})'
        x, p = self.x.sous(), self.p.sous()
        s += str(x) if x.appartient(Naturel) else f'({str(x)})'
        if p.sous() != un:
            s += '^'
            s += str(p) if p.appartient(Naturel) else f'({str(p)})'
        return s


def sqrt(r):
    return Puissance(r, Rationnel(1, 2)).sous()


class Complexe(Nombre):
    def __init__(self, x, y = 0):
        x, y = Nombre.ou_int(x), Nombre.ou_int(y)
        self.x = x.sous()
        self.y = y.sous()

    def __eq__(self, autre):
        if isinstance(autre, Expi):
            s = self.sur(Expi)
            if s is not None:
                return s == autre
        return (isinstance(autre, Complexe)
                and self.x == autre.x
                and self.y == autre.y)

    def sous(self):
        if self.y == zero:
            return self.x
        return self

    def _sur(self, E):
        try:
            a = self.arg()
        except ArithmeticError:
            return
        return Expi(a, module=abs(self))

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

    def arg(self):
        if self.y == zero: return self.x.arg()
        if self.x == zero:
            if self.y.signe() == 1: return pi / 2
            return -pi / 2
        if self.y.signe() == 1:
            if self.x == self.y: return pi / 4
            if self.x == -self.y: return (pi / 4) * 3
        if self.x == -self.y: return -pi/4
        if self.x == self.y: return (-pi / 4) * 3
        raise ArithmeticError(f'Extraction d\'argument impossible sur {self}')

    def __str__(self):
        sx = str(self.x)
        sy = str(self.y) if self.y.signe() == 1 else '-' + str(abs(self.y))
        sy += 'i'
        if self.y == un: sy = 'i'
        if self.y == -un: sy = '-i'
        if self.x == self.y == zero: return '0'
        if self.x == zero: return sy
        if self.y == zero: return sx
        return sx + ' + ' + sy


i = Complexe(zero, un)


def int_vers_bin(n: int, *, taille=None):
    assert n >= 0
    b = [int(i) for i in bin(n)[2:]]
    return b if taille is None else [0] * (taille - len(b)) + b


def bin_vers_int(*valeurs):
    return int(''.join([str(i) for i in valeurs]) or '0', base=2)


def int_log2(n: int):  # partie entière supérieure de log2(n)
    assert n > 0
    return len(bin(n)[2:])


def strbin_vers_int(s):
    return int(s, base=2)


def int_vers_strbin(n: int, *, taille=None):
    assert n >= 0
    s = bin(n)[2:]
    return s if taille is None else '0' * (taille - len(s)) + s


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

    def _sur(self, E):
        return Naturel(self.n).sur(E)

    @staticmethod
    def uplet(*valeurs):
        return F2Uplet(*valeurs)

    def __str__(self):
        return str(self.n)


class F2Uplet:
    def __init__(self, *valeurs):
        self.taille = len(valeurs)
        self._valeurs = [F2(i) for i in valeurs]

    def __eq__(self, autre):
        return (isinstance(autre, F2Uplet)
                and self.taille == autre.taille
                and all([self[i] == autre[i] for i in range(self.taille)]))

    def __add__(self, autre):
        assert isinstance(autre, F2Uplet) and self.taille == autre.taille
        return F2Uplet(*[self[i] + autre[i] for i in range(self.taille)])

    def __getitem__(self, indice):
        return self._valeurs[indice]

    def __setitem__(self, indice, valeur):
        assert isinstance(valeur, F2)
        self._valeurs[indice] = valeur

    def __int__(self):
        return bin_vers_int(*self._valeurs)

    def __str__(self):
        return '(' + ', '.join(str(i) for i in self._valeurs) + ')'


class Matrice(Nombre):
    def __init__(self, t):
        assert all([len(i) == len(t[0]) for i in t])
        self.p = len(t)
        self.q = len(t[0])
        self.forme = (self.p, self.q)
        self._c = [
            [Nombre.ou_int(t[i][j]) for j in range(self.q)]
            for i in range(self.p)
        ]

    def __eq__(self, autre):
        if (not isinstance(autre, Matrice)) or self.p != autre.p or self.q != autre.q:
            return False
        for i in range(self.p):
            for j in range(self.q):
                if self[i, j] != autre[i, j]:
                    return False
        return True

    def sous(self):
        return self

    # Renvoie une matrice remplie de zéros
    # p est la longueur de la matrice (nombre de lignes)
    # q est la largeur de la matrice (nombre de colonnes)
    @staticmethod
    def zeros(p, q = None):
        if q is None:
            q = p
        assert isinstance(p, int) and isinstance(q, int)
        return Matrice([[zero for _ in range(q)] for _ in range(p)])

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
        valeur = Nombre.ou_int(valeur)
        assert isinstance(valeur, Nombre), f'Pas un nombre : {valeur}'
        if isinstance(cle, tuple):
            i, j = cle
            assert isinstance(i, int) and 0 <= i < self.p
            assert isinstance(j, int) and 0 <= j < self.q
            self._c[i][j] = valeur
        else:
            assert isinstance(cle, int)
            if self.p == 1:
                self._c[0][cle] = valeur
            else:
                assert self.q == 1
                self._c[cle][0] = valeur

    def __add__(self, autre):
        assert self.p == autre.p
        assert self.q == autre.q
        return Matrice([
            [self[i, j] + autre[i, j] for j in range(self.q)]
            for i in range(self.p)
        ])

    def __mul__(self, autre):
        if isinstance(autre, Matrice):
            assert self.q == autre.p
            m = Matrice.zeros(self.p, autre.q)
            for i in range(self.p):
                for j in range(autre.q):
                    m[i, j] = zero
                    for k in range(self.q):
                        m[i, j] += self[i, k] * autre[k, j]
            return m
        autre = Nombre.ou_int(autre)
        if autre == zero: return Matrice.zeros(self.p, self.q)
        if autre == un: return self
        if autre == -un: return -self
        return Matrice([
            [autre * self[i, j] for j in range(self.q)]
            for i in range(self.p)
        ])

    def transposee(self):
        return Matrice([
            [self[j, i] for i in range(self.p)] for j in range(self.q)
        ])

    def conjuguee(self):
        return Matrice([
            [self[i, j].sur(Complexe).conjugue() for j in range(self.q)]
            for i in range(self.p)
        ])

    @staticmethod
    def scalaire(k, n):
        return Matrice([
            [k if i == j else zero for j in range(n)] for i in range(n)
        ])

    @staticmethod
    def identite(n):
        return Matrice.scalaire(un, n)

    @staticmethod
    def ligne(*args):
        l = []
        for i in args:
            if isinstance(i, list):
                l += i
            else:
                l.append(i)
        return Matrice([l])

    @staticmethod
    def colonne(*args):
        c = []
        for i in args:
            if isinstance(i, list):
                c += i
            else:
                c.append(i)
        return Matrice([[i] for i in c])

    # Correspond au produit tensoriel pour deux matrices (prod. de Kronecker)
    # S'utilise pour deux matrices A et B en écrivant A @ B.
    # se fait en complexité O(self.p * self.q * autre.p * autre.q)
    def __matmul__(self, autre):
        assert isinstance(autre, Matrice)
        c = lambda i, j: self[i // autre.p, j // autre.q] * autre[i % autre.p, j % autre.q]
        return Matrice([[c(i, j) for j in range(self.q * autre.q)] for i in range(self.p * autre.p)])

    def __pow__(self, exposant):
        exposant = int(exposant)
        if self == Matrice.identite(self.p) or exposant == 0:
            return Matrice.identite(self.p ** exposant)
        if self._c == [[un]]:
            return self
        if exposant == 1:
            return self
        a = self ** (exposant // 2)
        if exposant % 2 == 1:
            return self @ (a @ a)
        return a @ a

    def __str__(self):
        n = max([len(str(self[i, j])) for i in range(self.p) for j in range(self.q)])
        return '\n'.join([
            '( ' + ' '.join([
                str(self[i, j]).ljust(n) for j in range(self.q)
            ]) + ' )'
            for i in range(self.p)
        ])

    def __neg__(self):
        return Matrice([
            [-self[i, j] for j in range(self.q)] for i in range(self.p)
        ])


class VectPi(Nombre):  # pi * t avec t.appartient(Puissance)
    _float_pi = 3.141592653589793

    def __init__(self, t):
        t = Nombre.ou_int(t)
        assert t.appartient(Puissance)
        self.t = t

    def __float__(self):
        return VectPi._float_pi * float(self.t)

    def mod2pi(self):
        t = self.t.sur(Rationnel)
        if t is None:
            return self
        if t.num < 0:
            s = (self + (pi * 2))
            if s == zero:
                return zero
            return s.mod2pi()
        if t.num >= 2 * t.denom:
            s = (self - (pi * 2))
            if s == zero:
                return zero
            return s.mod2pi()
        return self

    def __eq__(self, autre):
        return (isinstance(autre, VectPi) and self.t == autre.t)

    def sous(self):
        if self.t == zero:
            return zero
        return self

    def __add__(self, autre):
        autre = Nombre.ou_int(autre)
        if autre == zero:
            return self
        if isinstance(autre, VectPi):
            return VectPi(self.t + autre.t).sous()
        raise Somme(self, autre, feuille=True)

    def __neg__(self):
        return VectPi(- self.t)

    def __mul__(self, autre):
        autre = Nombre.ou_int(autre)
        if autre.appartient(Puissance):
            return VectPi(self.t * autre).sous()
        raise MultiplicationErreur(self, autre)

    def __str__(self):
        if self.t == un: return 'π'
        if self.t == -un: return '-π'
        if self.t.appartient(Relatif):
            return f'{self.t}π'
        r = self.t.sur(Rationnel)
        if r is not None:
            return f'{r.num if r.num != 1 else ""}π/{r.denom}'
        return f'({self.t})*π'


class Expi(Nombre):  # module * exp(i * arg)
    def __init__(self, arg, *, module=un):
        arg, module = Nombre.ou_int(arg), Nombre.ou_int(module)
        assert arg.appartient(Puissance) or arg.appartient(VectPi)
        assert module.signe() == 1
        a = arg.sur(VectPi)
        if a is not None:
            self._arg = a.mod2pi()
        else:
            self._arg = arg
        self._module = module

    def __eq__(self, autre):
        return (isinstance(autre, Expi)
                and self.arg() == autre.arg()
                and abs(self) == abs(autre))

    def arg(self):
        return self._arg

    def sous_leger(self):
        a = self.arg()
        if a == zero: return un
        if abs(self) == zero: return zero
        if a.appartient(VectPi):
            if a.t.appartient(Relatif):
                return abs(self) * ((-un) ** self.arg().t)
            t = a.t.sur(Rationnel)
            if t is not None and t.denom == 2:
                if t.num == 1: return i
                if t.num == 3: return -i
        return self

    def sous(self):
        s = self.sous_leger()
        return s

    def _sur(self, E):
        sl = self.sous_leger()
        if not isinstance(sl, Expi):
            return sl.sur(E)
        sa = self.arg()
        if sa.appartient(VectPi):
            t = sa.t.sur(Rationnel)
            if t is not None and t.denom == 4:
                re = 1 if t.num in (1, 7) else -1
                im = 1 if t.num in (1, 3) else -1
                m = abs(self) * sqrt(un / 2)
                return Complexe(m * re, m * im).sur(E)

    def __abs__(self):
        return self._module

    def __mul__(self, autre):
        autre = Nombre.ou_int(autre)
        if autre.appartient(Puissance):
            if autre.signe() == 1:
                return Expi(self.arg(), module=abs(self) * autre).sous_leger()
            return Expi(self.arg() + pi, module=abs(self) * (-autre)).sous_leger()
        if isinstance(autre, Expi):
            return Expi(self.arg() + autre.arg(),
                        module=abs(self) * abs(autre)).sous_leger()
        if isinstance(autre, Complexe):
            s = autre.sur(Expi)
            if s is not None: return self * s
        raise MultiplicationErreur(self, autre)

    def __pow__(self, n):
        n = Nombre.ou_int(n)
        return Expi(self.arg() * n, module = abs(self) ** n).sous()

    def __add__(self, autre):
        if autre.sous() == zero:
            return self
        if isinstance(autre, Expi):
            if self.arg() == autre.arg():
                return Expi(self.arg(),
                            module = abs(self) + abs(autre))
            if self.arg() + pi == autre.arg():
                r = abs(self) - abs(autre)
                if r.signe() == 1:
                    return Expi(self.arg(), module=r).sous()
                return Expi(self.arg() + pi, module=-r).sous()
            if self.arg() == autre.arg() + pi:
                return autre + self
        s = self._sur(Complexe)
        if s is not None and self != s:
            return s + autre
        return Somme(self, autre, feuille=True)

    def __neg__(self):
        return Expi(self.arg() + pi, module=abs(self))

    def inverse(self):
        return Expi(-self.arg(), module=abs(self).inverse())

    def __str__(self):
        if abs(self) == un:
            return f'exp(i*({self.arg()}))'
        return f'{abs(self)}*exp(i*({self.arg()}))'


pi = VectPi(1)
def expi(theta): return Expi(theta).sous()

def somme(*termes):
    return Somme(*termes).sous()

class Somme(Nombre):
    # feuille: True si pas de simplifications à faire
    def __init__(self, *termes, feuille=False):
        assert isinstance(feuille, bool)
        self._pos = 0
        if feuille:
            self._termes = [Nombre.ou_int(i) for i in termes]
        else:
            self._termes = []
            for i in termes:
                self._ajoute_nombre(Nombre.ou_int(i))

    def __eq__(self, autre):
        if not isinstance(autre, Somme) or len(self) != len(autre):
            return False
        for i in self:
            if i not in autre._termes:
                return False
        return True

    def __len__(self):
        return len(self._termes)

    def sous(self):
        if len(self) == 1:
            return self._termes[0]
        return self

    def __add__(self, autre):
        if isinstance(autre, Somme):
            return self._plus_somme(autre)
        return self._plus_nombre(autre)

    def __mul__(self, autre):
        if isinstance(autre, Somme):
            return Somme(*[
                self._termes[i] * autre._termes[j]
                for i in range(len(self))
                for j in range(len(autre))
            ]).sous()
        return Somme(*[i * autre for i in self]).sous()

    def _plus_somme(self, autre):
        s = Somme(*[i for i in self])
        for j in autre:
            s += j
        return s.sous()

    def _ajoute_nombre(self, autre):
        for i in range(len(self)):
            k = self._termes[i] + autre
            if not isinstance(k, Somme):
                self._termes.pop(i)
                self._ajoute_nombre(k)
                break
        else:
            self._termes.append(autre)

    def _plus_nombre(self, autre):
        r = Somme(*[i for i in self])
        r._ajoute_nombre(autre)
        return r.sous()

    def __iter__(self):
        self._pos = 0
        return self

    def __next__(self):
        if self._pos < len(self):
            self._pos += 1
            return self._termes[self._pos-1]
        raise StopIteration

    def __neg__(self):
        return Somme(*[-i for i in self])

    def signe(self):
        return 1

    def __float__(self):
        return sum(float(i) for i in self)

    def __sub__(self, autre):
        return self + (- autre)

    def __str__(self):
        return ' + '.join(str(i) for i in self)

    def __repr__(self):
        return '∑[' + ' + '.join(str(i) for i in self) + ']'
