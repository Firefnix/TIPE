from enum import Enum, auto
from random import choices, gauss, uniform

# Représente la polarisation d'un photon or l'orientation d'un filtre
class Polarisation(Enum):
    D = auto()
    R = auto()

class Loi:
    def __init__(self, generateur):
        self.generateur = generateur

    def nombre(self):
        return self.generateur()

    @staticmethod
    def gaussienne(moyenne, ecart_type):
        return Loi(lambda: gauss(moyenne, ecart_type))

    @staticmethod
    def uniforme():
        return Loi(lambda: uniform(0, 1))

    def polarisation(self):
        k = self.nombre()
        return list(Polarisation)[int(k * len(Polarisation))]

class Photon:
    def __init__(self, loi):
        self.loi = loi
        self.est_effondre = False
        self.pol = None
        self.copains = [self] # tout photon est intriqué avec lui-même

    def mesure(self):
        if self.est_effondre:
            return self.pol

        self.pol = self.loi.polarisation()
        self.est_effondre = True

        for i in self.copains:
            i.effondrer(self.pol)
        return self.pol

    def effondrer(self, pol):
        self.pol = pol

    def intrique_avec_tous(self, autres):
        for i in autres:
            self.intrique_avec(self)

    def intrique_avec(self, autre):
        self.copains.append(autre)
        autre.copains.append(self)


# Un filre à photons
#
# Ne sélectionne que les photons de polarisation égale à `orientation`.
class Polariseur:
    def __init__(self, orientation):
        self.orientation = orientation

    def passe(self, photon):
        return photon.mesure() == self.orientation

    def filtre(self, photons):
        return [i for i in photons if self.passe(i)]


# Une source lumineuse
#
# Par défaut, la loi gouvernant chaque photon est uniforme.
class Source:
    def __init__(self, loi = Loi.uniforme()):
        self.loi = loi

    def photons(self, N):
        return [self.photon() for i in range(N)]

    def photon(self):
        return Photon(self.loi)

S = Source()
l = S.photons(100)
l[0].intrique_avec_tous(l)
P = Polariseur(Polarisation.D)
lp = P.filtre(l)
print(len(lp))
