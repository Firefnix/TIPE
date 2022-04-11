# Du 'binaire' est représenté par une liste de 0 et de 1 (entiers).
# Une 'lettre' est une chaîne de caractères de longueur 1.
# Un mot est une chaîne de caractères de longueur >= 1 (suite de lettres).

taille_lettre = 5 # le nombre de bits par lettre

def lettre_vers_binaire(lettre):
    assert len(lettre) == 1
    binaire = [int(i) for i in bin(disco[lettre])[2:]]
    while len(binaire) < 5:
        binaire = [0] + binaire # toujours de taille 5
    return binaire

def binaire_vers_lettre(binaire):
    assert len(binaire) == 5
    n = int(''.join([str(i) for i in binaire]), base=2)
    for lettre in disco:
        if disco[lettre] == n:
            return lettre

def mot_vers_binaire(mot):
    binaire = []
    for lettre in mot:
        binaire += lettre_vers_binaire(lettre)
    return binaire

def binaire_vers_mot(binaire):
    assert len(binaire) % 5 == 0
    mot = ''
    for i in range(len(binaire) // 5):
        mot += binaire_vers_lettre(binaire[5*i:5*(i+1)])
    return mot

disco = {
    'Fin': 0,
    'a': 1,
    'b': 2,
    'c': 3,
    'd': 4,
    'e': 5,
    'f': 6,
    'g': 7,
    'h': 8,
    'i': 9,
    'j': 10,
    'k': 11,
    'l': 12,
    'm': 13,
    'n': 14,
    'o': 15,
    'p': 16,
    'q': 17,
    'r': 18,
    's': 19,
    't': 20,
    'u': 21,
    'v': 22,
    'w': 23,
    'x': 24,
    'y': 25,
    'z': 26,
    ' ': 27,
    '.': 28,
    ',': 29,
    "'": 30,
    '?': 31,
    'Début': 32,
}
