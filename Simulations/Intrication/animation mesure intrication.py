import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

fig, ax = plt.subplots()
plt.axis('square')

photons = {} 
for i in range(-10, 11, 2):
    photons[i], = ax.plot([], [], ls = 'none', marker = 'o', color = 'purple')

plt.xlim(-10,10)
plt.ylim(-10.5,10.5)

N = 300
X = np.linspace(-10, 10, N)
color = ['blue', 'green']

plt.plot([0,0], [10,-10], color = 'black')


def animate(i):
    for c in photons:
        photons[c].set_data(X[i], c)

        if abs(photons[c].get_xdata()) <= 10**-1:
                photons[c].set_color(random.choice(color))

    return tuple(photons[c] for c in photons)

ani = animation.FuncAnimation(fig, animate, frames=range(N), blit = True, interval = 5, repeat = False)
plt.show()