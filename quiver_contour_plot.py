# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.patches import Circle


# %%
#output settings
np.set_printoptions(precision=2)
# get_ipython().run_line_magic('matplotlib', 'qt')


# %%
#the grid

Nq = 30
Nth = 30
Rs = 1.

Q, TH = np.linspace(0, Rs, Nq), np.linspace(0, np.pi, Nth)          #compact polar coordinates 
R = Rs**2/Q                                                         #normal polar coordinates
X, Z = R*np.sin(TH), R*np.cos(TH)                                   #cartesian coordinates

q, th = np.meshgrid(Q, TH)                                          #2d meshgrid
r = Rs**2/q
x, z = r*np.sin(th), r*np.cos(th)


# %%
#the magnetic field

Pdip = np.sin(th)**2/r          #the poloidal flux function

Br = -2*np.cos(th)/r**3           #the magnetic field in polar
Bth = -np.sin(th)/r**3

Bx = -3*np.cos(th)*np.sin(th)/r**3          #the magnetic field projected in cartesian
Bz = (1-3*np.cos(th)**2)/r**3

Bmag = np.sqrt(Bx**2+Bz**2)
# Bx = -3*x*z/r**
# Bz = -(3*z**2-r**2)/r**5


# %%
#cartesian plot

fig, ax = plt.subplots()

ax.contour(x, z, Pdip, levels=25, cmap=cm.spring)            #contours of flux function

ax.quiver(x, z, Bx/Bmag, Bz/Bmag, pivot='tail', angles='xy', scale_units='xy', scale=15., headaxislength=3.5)                            #vector field of B

ax.set_xlim(0, 4)
ax.set_ylim(-2., 2.)
ax.set_xlabel('x')
ax.set_ylabel('z')
ax.set_aspect('equal')

ax.add_patch(Circle((0.,0.), Rs, color='b', zorder=-1))
plt.show()

# %%
#polar plot

# fig1 = plt.figure()
# ax1 = fig1.add_subplot('111', projection='polar')

# ax1.contour(th, r, Pdip)
# # ax1.quiver(th, r, Bth, Br)            #in the polar plot this generally does NOT work, not exclusively for this case

# ax1.set_ylim(0, 5)
# ax1.set_theta_direction(-1)
# ax1.set_theta_zero_location('N')


# %%



