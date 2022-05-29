from qubit import bra, ket
from portes import H, S

e0 = ket(1,1,1,0)
e1 = e0 >> H**4
e2 = e1 >> S**2
e3 = e2 >> H**4

print('État 0 :', e0)
print('État 1 :', e1)
print('État 2 :', e2)
print('État 3 :', e3)
print (e0>>S**2)

print(bra(0) | (ket(0)>>H))
