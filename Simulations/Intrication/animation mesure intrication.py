import random
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

fig, ax = plt.subplots()
plt.axis('square')

N_item = 5 #nombre de photons à animer

photons = {}
for i in range(N_item):
    photons[i], = ax.plot([], [], ls = 'none', marker = 'o', color = 'purple')

plt.xlim(-10,10)
plt.ylim(-10.5,10.5)

N = 300 #résulution de l'échantillonage de (Ox)
disp = 20 #coeff d'écartement
base = np.linspace(-10, 10, N)
x_pol_1 = -2
x_pol_2 = 4
X = {}
for i in range(N_item):
    X[i] = np.concatenate((np.full(disp*i, -10), np.linspace(-10, 10, N), np.full(N, 10)), axis = None)
color = ['blue', 'green']

plt.plot([x_pol_1,x_pol_1], [10.5,-10.5], color = 'black')
plt.plot([x_pol_2,x_pol_2], [10.5,-10.5], color = 'black')

ax.set_xticklabels([])
ax.set_yticklabels([])

plt.tick_params(axis = 'x', length = 0)
plt.tick_params(axis = 'y', length = 0)

key = ['0'] * N_item

def list_to_str(l):
    ret = ""
    for e in l:
        ret = ret + e
    return ret

text = {}
text[0] = ax.text(4, 4, list_to_str(key), fontsize = 15, fontweight = 'bold', color = 'black')
ax.add_patch(Rectangle((8, -1), 2, 2))

def ret_tuple(dico):
    return tuple(dico[c] for c in dico)

def animate(i):
    for c in photons:
        photons[c].set_data(X[c][i], 0)

        if abs(photons[c].get_xdata() + 10) <= 10**-1:
                photons[c].set_color('purple')

        if abs(photons[c].get_xdata() - x_pol_1) <= 10**-1:
                photons[c].set_color(random.choice(color))

        if abs(photons[c].get_xdata() - x_pol_2) <= 10**-1 and photons[c].get_color() == 'green':
            photons[c].set_alpha(0.0)

        if abs(photons[c].get_xdata() - 8) <= 10**-1 and photons[c].get_color() != 'white':
            key[c] = '1'
            text[0].set_text(list_to_str(key))

    return ret_tuple(photons) + tuple(text[c] for c in text)

ani = animation.FuncAnimation(fig, animate, frames=range(2*N), blit = True, interval = 5, repeat = False)
plt.show()
